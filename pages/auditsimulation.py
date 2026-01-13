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

from agents.agent_loader import get_agent
from agents.context_agent import assign_user_input, AssignResponseInput, assign_user_input_to_response_option, \
    ask_next_question, AssignUserResponseInput, NextResponseInput, help_user_to_response
from agents.rating_agent import BewertungEingabe, evaluate_phase_and_get_response
from agents.retrieval_agent import chat_agent
from agents.welcome_agent import get_welcome_message, start_simulation
from audit_process.general import Phasen, get_no_expert_condition, get_method_search_string, get_method_user_input, \
    get_ai_tool_condition, get_ai_tool_search_query, get_ai_tool_user_input
from audit_process.organizing import organizing_questions, organzing_response_text_options, organizing_response_q1, \
    organizing_response_q2, organizing_response_q3, organzing_rating_metrik, organizing_response_q4, organizing_examples
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
st.sidebar.page_link('pages/simulation-organizing.py', label='Audit Simulation')
st.sidebar.page_link('pages/auditsimulation.py', label='KI Auditsimuation')

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
    print("store messages")
    print(st.session_state.messages)
    print(messages)
    for msg in messages:
        if isinstance(msg, ModelResponse):
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

                        st.session_state.messages.append(model_response)
                        return
            st.session_state.messages.append(msg)

def store_output_information(output_string):
    try:
        output_data = json.loads(output_string)
    except json.JSONDecodeError as e:
        st.error(f"Fehler beim Parsen des Agenten-Outputs: {e}")
        return

    if st.session_state.chat_state in [ChatState.WELCOME, ChatState.START_SIMULATION]:
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
    async with get_welcome_message(Phasen.ORGANIZING.value) as response:
        async for output in response.stream_output():
            yield output

    add_response_messages_to_history(response.new_messages())



async def run_simulation_agent_with_streaming(userinput, frage):
    async with start_simulation(userinput, frage, st.session_state.messages) as response:

        async for output in response.stream_output():
            yield output

    add_response_messages_to_history(response.new_messages())

async def run_retrieval_agent_with_streaming(user_input, use_history=True, add_message=True):
    async with chat_agent.run_stream(
        user_input,
        deps=st.session_state.agent_deps,
        message_history=st.session_state.org_chat_messages if use_history else None
    ) as result:
        async for message in result.stream_text(delta=True):
            yield message

    if add_message:
        st.session_state.org_chat_messages.extend(result.new_messages())

def get_agent_input(userinput):
    return AssignUserResponseInput(
        frage=organizing_questions[st.session_state.o_question_index],
        nutzereingabe=userinput,
        antwortoptionen=organzing_response_text_options[st.session_state.o_question_index],
        example=organizing_examples[st.session_state.o_question_index]
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
        async with help_user_to_response(help_input, st.session_state.messages) as response:
            async for output in response.stream_output():
                yield output
    elif st.session_state.o_question_index < len(organizing_questions) - 1:
        next_input = NextResponseInput(
            frage=organizing_questions[st.session_state.o_question_index],
            nutzereingabe=userinput,
            naechste_frage=organizing_questions[st.session_state.o_question_index + next_question]
        )

        async with ask_next_question(next_input, st.session_state.messages) as response:
            async for output in response.stream_output():
                yield output

        if st.session_state.o_question_index == 0:
            st.session_state.ux_experience = assign_agent_response.output.zugeordnete_antwort
        elif st.session_state.o_question_index == 1:
            st.session_state.company_size = assign_agent_response.output.zugeordnete_antwort
        elif st.session_state.o_question_index == 3:
            st.session_state.have_ux_expert = assign_agent_response.output.zugeordnete_antwort
        else:
            st.session_state.assigned_responses.append(assign_agent_response.output.zugeordnete_antwort)
        st.session_state.o_question_index += next_question

    else:
        raise ValueError('Invalid chat state')

    add_response_messages_to_history(response.new_messages())

async def run_report_generation_with_streaming(ai_tools, methods):
    print("responses")
    print(st.session_state.assigned_responses)

    a1 = next(a for a in organizing_response_q1 if a.text == st.session_state.assigned_responses[0])
    a2 = next(a for a in organizing_response_q2 if a.text == st.session_state.assigned_responses[1])
    a3 = next(a for a in organizing_response_q3 if a.text == st.session_state.assigned_responses[2])
    a4 = next(a for a in organizing_response_q4 if a.text == st.session_state.assigned_responses[3])

    async with evaluate_phase_and_get_response(
        nutzereingabe=st.session_state.o_user_inputs,
        antworten=BewertungEingabe(antwortoptionen=[a1, a2, a3, a4]),
        phase=Phasen.ORGANIZING.value,
        ux_erfahrung=st.session_state.ux_experience,
        methoden=methods, ki_tools=ai_tools, evaluation_metrik=organzing_rating_metrik
    ) as response:
        async for output in response.stream_output():
            yield output

    add_response_messages_to_history(response.new_messages())



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


async def main():
    st.title("Nutzerzentriert Entwickelt")

    # Initialize chat history in session state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "assigned_responses" not in st.session_state:
        st.session_state.assigned_responses = []

    if "have_ux_expert" not in st.session_state:
        st.session_state.have_ux_expert = False

    if "ux_experience" not in st.session_state:
        st.session_state.ux_experience = ''

    if "company_size" not in st.session_state:
        st.session_state.company_size = ''

    if "agent_deps" not in st.session_state:
        with st.spinner("Initialisiere Agent..."):
            st.session_state.agent_deps = get_agent()

    if "chat_state" not in st.session_state:
        st.session_state.chat_state = ChatState.WELCOME

    if "o_question_index" not in st.session_state:
        st.session_state.o_question_index = 0

    if "o_user_inputs" not in st.session_state:
        st.session_state.o_user_inputs = []

    if "simulation_started" not in st.session_state:
        st.session_state.simulation_started = False
        # Display all messages from the conversation so far
    # Each message is either a ModelRequest or ModelResponse.
    # We iterate over their parts to decide how to display them.
    for msg in st.session_state.messages:
        if isinstance(msg, ModelRequest) or isinstance(msg, ModelResponse):
            for part in msg.parts:
                display_message_part(part)

    if st.session_state.chat_state == ChatState.WELCOME:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""
            output_string = ""
            stream_antworttext = True

            async for chunk in run_welcome_agent_with_streaming():
                output_string = chunk
                if stream_antworttext:
                    full = chunk.antworttext
                    placeholder.markdown(full + "▌")

                # Stoppe das Streaming, sobald der Text abgeschlossen ist
                if '",' in chunk:
                    stream_antworttext = False

            placeholder.markdown(full)
            st.session_state.simulation_started = output_string.simulation_gestartet

        st.session_state.chat_state = ChatState.START_SIMULATION

    if st.session_state.simulation_started:
        st.session_state.chat_state = ChatState.GET_CONTEXT_INFO
    # Chat input for the user
    user_input = st.chat_input("What do you want to know?")

    if user_input:
        # Display user prompt in the UI
        with st.chat_message("user"):
            st.session_state.o_user_inputs.append(user_input)
            st.markdown(user_input)
            st.session_state.messages.extend(
                [ModelRequest(parts=[UserPromptPart(content=user_input)])])

        assign_agent_response = await assign_response(user_input)
        print(st.session_state.o_question_index)
        print(len(organizing_questions))

        if assign_agent_response.output.zugeordnete_antwort and st.session_state.o_question_index == len(organizing_questions) - 1:
            st.session_state.chat_state = ChatState.CREATE_REPORT
            st.session_state.assigned_responses.append(assign_agent_response.output.zugeordnete_antwort)

            with st.spinner("Die Bewertung wird jetzt ausgeführt das kann einige Zeit dauern."):
                ai_tools = await  get_ai_tool()
                methods = await get_methods()
                print(ai_tools)
                print(methods)
        # Display the assistant's partial response while streaming

        with st.chat_message("assistant"):
            # Create a placeholder for the streaming text
            message_placeholder = st.empty()
            full = ""
            output_string = ""
            stream_antworttext = True

            # Properly consume the async generator with async for
            print(st.session_state.chat_state)
            if st.session_state.chat_state == ChatState.START_SIMULATION:
                generator = run_simulation_agent_with_streaming(user_input, organizing_questions[0])
            elif st.session_state.chat_state == ChatState.GET_CONTEXT_INFO:
                generator = run_context_agent_with_streaming(user_input, assign_agent_response)
            elif st.session_state.chat_state == ChatState.CREATE_REPORT:
                generator = run_report_generation_with_streaming(ai_tools, methods)
            else:
                raise ValueError('Invalid chat state')

            async for chunk in generator:
                output_string = chunk

                if stream_antworttext:
                    full = chunk.antworttext
                    message_placeholder.markdown(full + "▌")
                if '",' in chunk:
                    stream_antworttext = False

            message_placeholder.markdown(full)
            print("Output:")
            print(output_string)

            if st.session_state.chat_state == ChatState.START_SIMULATION:
                st.session_state.simulation_started = output_string.simulation_gestartet

                if st.session_state.simulation_started:
                    print("Start context inquery")
                    st.session_state.chat_state = ChatState.GET_CONTEXT_INFO



if __name__ == "__main__":
    asyncio.run(main())
