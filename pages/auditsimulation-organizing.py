import json
import re
from enum import Enum, auto

from docutils.nodes import Part
from dotenv import load_dotenv
import streamlit as st
import asyncio

from pydantic_ai import TextPart
# Import all the message part classes
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse, ToolCallPart, UserPromptPart
)
from streamlit_float import float_parent, float_init, float_css_helper

from agents.agent_loader import get_agent
from agents.context_agent import assign_user_input, AssignResponseInput, assign_user_input_to_response_option, \
    ask_next_question, AssignUserResponseInput, NextResponseInput, help_user_to_response
from agents.rating_agent import BewertungEingabe, evaluate_phase_and_get_response, get_final_report
from agents.retrieval_agent import chat_agent, run_rag_agent_with_evaluation_logic
from agents.welcome_agent import get_welcome_message, start_simulation
from audit_process.general import Phasen, get_no_expert_condition, get_method_search_string, get_method_user_input, \
    get_ai_tool_condition, get_ai_tool_search_query, get_ai_tool_user_input
from audit_process.organizing import organizing_questions, organzing_response_text_options, organizing_response_q1, \
    organizing_response_q2, organizing_response_q3, organzing_rating_metrik, organizing_response_q4, \
    organizing_examples, organzing_rating_metrik_with_help
from ui.html import get_final_review_html
from utils import extract_assistant_response_text_from_output


class ChatState(str, Enum):
    WELCOME = "Welcome"
    START_SIMULATION = "Start Simulation"
    GET_CONTEXT_INFO = "Get Context Info"
    CREATE_REPORT = "Create Report"
    FOLLOW_UP = "Follow-Up"

load_dotenv()

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/auditsimulation-organizing.py', label='KI-Audit: Organisieren')

float_init()



async def run_final_report_generation():
    async with get_final_report(
            phase=Phasen.ORGANIZING.value,
            groesse=st.session_state.company_size,
            ux_erfahrung=st.session_state.ux_experience,
            pre_evaluation=st.session_state.organizing_report,
            message_history=st.session_state.organizing_messages
    ) as response:
        final_text = await response.get_output()
        print(final_text)
        return final_text



with st.container():

    if st.button(
            "Wechsle in die nächste Phase",
            use_container_width=True,
            disabled=not st.session_state.get("organizing_evaluation_finished", False),
            type="primary",
            key="next_phase_btn",
    ):
        print("Final Report")
        final_report = asyncio.run(run_final_report_generation())

        st.session_state.evaluation_report = final_report.antworttext
        st.switch_page("pages/auditsimulation-understanding.py")

    # WICHTIG: fixed + z-index + background, damit er wirklich "immer oben" bleibt
    float_parent(css="""
        position: fixed;
        top: 5rem;
        right: 5%;
        width: 20%;
        height: 2.5rem;
        z-index: 9999;
        background: white;
    """)


with st.container():
    st.download_button(
        label="Download als HTML",
        data=get_final_review_html(st.session_state.get("evaluation_report")),
        file_name="audit_report_document.html",
        mime="text/html",
        disabled = not st.session_state.get("organizing_evaluation_finished", False)
    )
    button_css = float_css_helper(width="37%", top="5rem", right="0%", transition=0)
    float_parent(css=button_css)

st.title("Nutzerzentriert Entwickelt")

def display_message_part(part):
    """
    Display a single part of a message in the Streamlit UI.
    Customize how you display system prompts, user prompts,
    tool calls, tool returns, etc.
    """

    # user-prompt
    if part.part_kind == 'user-prompt':
        with st.chat_message("user"):
            st.markdown(part.content)
    # text
    elif part.part_kind == 'text':
        with st.chat_message("assistant"):
            st.markdown(part.content)


def add_response_messages_to_history(messages):
    for msg in messages:
        if isinstance(msg, ModelResponse):
            for part in msg.parts:
                if isinstance(part, ToolCallPart):
                    output = part.args_as_dict()
                    response_text = output.get("antworttext", "")

                    text_part = TextPart(content=response_text)
                    # ModelResponse mit einem Text-Part
                    model_response = ModelResponse(
                        parts=[text_part]
                    )

                    st.session_state.organizing_messages.append(model_response)
                    return

            st.session_state.organizing_messages.append(msg)

def add_text_response_messages_to_history(messages):
    for msg in messages:
        if isinstance(msg, ModelResponse):
            for part in msg.parts:
                if isinstance(part, TextPart):
                    st.session_state.organizing_messages.append(msg)


def store_output_information(output_string):
    try:
        output_data = json.loads(output_string)
    except json.JSONDecodeError as e:
        st.error(f"Fehler beim Parsen des Agenten-Outputs: {e}")
        return

    if st.session_state.organizing_chat_state in [ChatState.WELCOME, ChatState.START_SIMULATION]:
        st.session_state.simulation_started = output_data['simulation_gestartet']

async def get_methods():
    if not st.session_state.have_ux_expert:
        st.session_state.agent_deps.condition = get_no_expert_condition()
    st.session_state.agent_deps.explicit_search_query = get_method_search_string(Phasen.ORGANIZING.value)
    methods = ""
    async for message in run_retrieval_agent_with_streaming(user_input=get_method_user_input(Phasen.ORGANIZING.value),
                                                  use_history=False, add_message=False):
        methods += message

    st.session_state.agent_deps.condition = None
    st.session_state.agent_deps.explicit_search_query = None

    return methods

async def get_ai_tool():
    st.session_state.agent_deps.condition = get_ai_tool_condition()
    st.session_state.agent_deps.explicit_search_query = get_ai_tool_search_query(Phasen.ORGANIZING.value)

    ai_tools = ""
    async for message in run_retrieval_agent_with_streaming(get_ai_tool_user_input(Phasen.ORGANIZING.value), use_history=False,
                                                  add_message=False):
        ai_tools += message

    st.session_state.agent_deps.condition = None
    st.session_state.agent_deps.explicit_search_query = None

    return ai_tools

async def run_welcome_agent_with_streaming():
    async with get_welcome_message(Phasen.ORGANIZING.value, organizing_questions[0]) as response:
        async for output in response.stream_output():
            yield output

    add_response_messages_to_history(response.new_messages())



async def run_simulation_agent_with_streaming(userinput, frage):
    async with start_simulation(userinput, frage, st.session_state.organizing_messages) as response:

        async for output in response.stream_output():
            yield output

    add_response_messages_to_history(response.new_messages())

async def run_retrieval_agent_with_streaming(user_input, use_history=True, add_message=True):
    async with chat_agent.run_stream(
        user_input,
        deps=st.session_state.agent_deps,
        message_history=st.session_state.chat_messages if use_history else None
    ) as result:
        async for message in result.stream_text(delta=True):
            yield message

    if add_message:
        st.session_state.org_chat_messages.extend(result.new_messages())

def get_agent_input(userinput):
    return AssignUserResponseInput(
        frage=organizing_questions[st.session_state.organizing_question_index],
        nutzereingabe=userinput,
        antwortoptionen=organzing_response_text_options[st.session_state.organizing_question_index],
        example=organizing_examples[st.session_state.organizing_question_index]
    )

async def assign_response(userinput):
    return await assign_user_input_to_response_option(get_agent_input(userinput))

async def run_context_agent_with_streaming(userinput, assign_agent_response):

    help_input = get_agent_input(userinput)

    next_question = 1

    if assign_agent_response.output.zugeordnete_antwort == organizing_response_q1[1].text:
        next_question = 2
        st.session_state.have_ux_expert = True

    if assign_agent_response.output.zugeordnete_antwort is None:
        async with help_user_to_response(help_input, st.session_state.organizing_messages) as response:
            async for output in response.stream_output():
                yield output
    elif st.session_state.organizing_question_index < len(organizing_questions) - 1:
        next_input = NextResponseInput(
            frage=organizing_questions[st.session_state.organizing_question_index],
            nutzereingabe=userinput,
            naechste_frage=organizing_questions[st.session_state.organizing_question_index + next_question]
        )

        async with ask_next_question(next_input, st.session_state.organizing_messages) as response:
            async for output in response.stream_output():
                yield output

        if st.session_state.organizing_question_index == 0:
            st.session_state.ux_experience = assign_agent_response.output.zugeordnete_antwort
        elif st.session_state.organizing_question_index == 1:
            st.session_state.company_size = assign_agent_response.output.zugeordnete_antwort
        elif st.session_state.organizing_question_index == 3:
            st.session_state.have_ux_expert = assign_agent_response.output.zugeordnete_antwort
        else:
            st.session_state.organizing_assigned_responses.append(assign_agent_response.output.zugeordnete_antwort)
        st.session_state.organizing_question_index += next_question

    else:
        raise ValueError('Invalid chat state')

    add_response_messages_to_history(response.new_messages())

async def run_report_generation_with_streaming(ai_tools, methods):

    a1 = next(a for a in organizing_response_q1 if a.text == st.session_state.organizing_assigned_responses[0])
    a2 = next(a for a in organizing_response_q2 if a.text == st.session_state.organizing_assigned_responses[1])
    a3 = next(a for a in organizing_response_q3 if a.text == st.session_state.organizing_assigned_responses[2])
    a4 = next(a for a in organizing_response_q4 if a.text == st.session_state.organizing_assigned_responses[3])

    async with evaluate_phase_and_get_response(
        nutzereingabe=st.session_state.organizing_user_inputs,
        antworten=BewertungEingabe(antwortoptionen=[a1, a2, a3, a4]),
        phase=Phasen.ORGANIZING.value,
        groesse=st.session_state.company_size,
        ux_erfahrung=st.session_state.ux_experience,
        methoden=methods, ki_tools=ai_tools, evaluation_metrik=organzing_rating_metrik
    ) as response:
        async for output in response.stream_output():
            yield output

    st.session_state.organizing_evaluation_finished = True
    add_response_messages_to_history(response.new_messages())



async def run_post_agent_with_streaming(user_input, use_history=True, add_message=True):

    async with run_rag_agent_with_evaluation_logic(
        nutzereingabe=user_input,
        groesse=st.session_state.company_size,
        ux_erfahrung=st.session_state.ux_experience,
        agent_deps=st.session_state.agent_deps,
        message_history=st.session_state.organizing_messages if use_history else None,
        evaluation_metrik=organzing_rating_metrik_with_help
    ) as result:
        async for message in result.stream_text(delta=True):
            yield message
    add_text_response_messages_to_history(result.new_messages())


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


async def main():

    # Initialize chat history in session state if not present
    if "organizing_messages" not in st.session_state:
        st.session_state.organizing_messages = []

    if "organizing_assigned_responses" not in st.session_state:
        st.session_state.organizing_assigned_responses = []

    if "have_ux_expert" not in st.session_state:
        st.session_state.have_ux_expert = False

    if "ux_experience" not in st.session_state:
        st.session_state.ux_experience = ''

    if "company_size" not in st.session_state:
        st.session_state.company_size = ''

    if "agent_deps" not in st.session_state:
        with st.spinner("Initialisiere Agent..."):
            st.session_state.agent_deps = get_agent()

    if "organizing_chat_state" not in st.session_state:
        st.session_state.organizing_chat_state = ChatState.WELCOME

    if "organizing_question_index" not in st.session_state:
        st.session_state.organizing_question_index = 0

    if "organizing_user_inputs" not in st.session_state:
        st.session_state.organizing_user_inputs = []

    if "organizing_evaluation_finished" not in st.session_state:
        st.session_state.organizing_evaluation_finished = False

    if "organizing_button_updated" not in st.session_state:
        st.session_state.organizing_button_updated = True

    if "organizing_report" not in st.session_state:
        st.session_state.organizing_report = ""

    if "evaluation_report" not in st.session_state:
        st.session_state.evaluation_report = ""


        # Display all messages from the conversation so far
    # Each message is either a ModelRequest or ModelResponse.
    # We iterate over their parts to decide how to display them.
    for msg in st.session_state.organizing_messages:
        if isinstance(msg, ModelRequest) or isinstance(msg, ModelResponse):
            for part in msg.parts:
                display_message_part(part)

    if st.session_state.organizing_chat_state == ChatState.WELCOME:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_start = ""
            stream_antworttext = True

            async for chunk in run_welcome_agent_with_streaming():
                if stream_antworttext:
                    full_start = chunk.antworttext
                    placeholder.markdown(full_start + "▌")

                # Stoppe das Streaming, sobald der Text abgeschlossen ist
                if '",' in chunk:
                    stream_antworttext = False

            placeholder.markdown(full_start)

        st.session_state.organizing_chat_state = ChatState.GET_CONTEXT_INFO
        st.rerun()

    # Chat input for the user
    user_input = st.chat_input(key='content_input', placeholder="Was möchtest du wissen?")

    if user_input:
        # Display user prompt in the UI
        with st.chat_message("user"):
            st.session_state.organizing_user_inputs.append(user_input)
            st.markdown(user_input)
            st.session_state.organizing_messages.extend(
                [ModelRequest(parts=[UserPromptPart(content=user_input)])])

        assign_agent_response = await assign_response(user_input)

        print("Fragen:")
        print(st.session_state.organizing_question_index)
        print(len(organizing_questions))

        print("Zugeordnete Antwort:")
        print(assign_agent_response.output.zugeordnete_antwort)

        if assign_agent_response.output.zugeordnete_antwort and st.session_state.organizing_question_index == len(organizing_questions) - 1:
            st.session_state.organizing_chat_state = ChatState.CREATE_REPORT
            st.session_state.organizing_assigned_responses.append(assign_agent_response.output.zugeordnete_antwort)

            with st.spinner("Die Bewertung wird jetzt ausgeführt das kann einige Zeit dauern."):
                ai_tools = await  get_ai_tool()
                methods = await get_methods()

        # Display the assistant's partial response while streaming

        with st.chat_message("assistant"):
            # Create a placeholder for the streaming text
            message_placeholder = st.empty()
            full = ""
            output_string = ""
            stream_antworttext = True

            # Properly consume the async generator with async for
            print(st.session_state.organizing_chat_state)
            if st.session_state.organizing_chat_state == ChatState.START_SIMULATION:
                generator = run_simulation_agent_with_streaming(user_input, organizing_questions[0])
            elif st.session_state.organizing_chat_state == ChatState.GET_CONTEXT_INFO:
                generator = run_context_agent_with_streaming(user_input, assign_agent_response)
            elif st.session_state.organizing_chat_state == ChatState.CREATE_REPORT:
                generator = run_report_generation_with_streaming(ai_tools, methods)
            elif st.session_state.organizing_chat_state == ChatState.FOLLOW_UP:
                generator = run_post_agent_with_streaming(user_input)
            else:
                raise ValueError('Invalid chat state')

            async for chunk in generator:
                output_string = chunk

                if st.session_state.organizing_chat_state == ChatState.FOLLOW_UP:
                    full += chunk
                    message_placeholder.markdown(full + "▌")
                else:
                    if stream_antworttext:
                        full = chunk.antworttext
                        message_placeholder.markdown(full + "▌")
                    if '",' in chunk:
                        stream_antworttext = False

            message_placeholder.markdown(full)
            if st.session_state.organizing_chat_state == ChatState.CREATE_REPORT:
                print(full)
                st.session_state.organizing_report = full
                st.session_state.organizing_chat_state = ChatState.FOLLOW_UP

            if st.session_state.organizing_evaluation_finished and st.session_state.organizing_button_updated:
                st.session_state.organizing_button_updated = False
                st.rerun()



if __name__ == "__main__":
    asyncio.run(main())


