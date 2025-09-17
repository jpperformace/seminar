import textwrap
from typing import Optional

from dotenv import load_dotenv
from streamlit_float import *
from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart
import asyncio

from agents.agent_loader import get_agent
from agents.context_agent import AssignResponseInput, assign_user_input
from agents.rating_agent import evaluate_phase, BewertungEingabe
from agents.retrieval_agent import chat_agent
from audit_process.general import response_options_UX_experience, response_options_expert, get_method_condition, \
    get_method_search_string, get_method_user_input, Phasen, get_ai_tool_condition, get_ai_tool_search_query, \
    get_ai_tool_user_input, get_no_expert_condition
from ui.css import get_header_css, get_menu_css, get_review_container_css, get_download_button_css
from ui.html import get_new_review_text, get_default_hint_text, get_review_heading, get_header_html, \
    get_padding_html, get_tertiary_button_html, get_menu_heading_html, get_review_html, get_sidebar_html, \
    get_final_review_html
from audit_process.organizing import organizing_response_q1, organizing_response_q3, \
    organizing_response_q2, organizing_questions, organizing_summary, organzing_response_text_options, \
    organzing_rating_metrik

load_dotenv()

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/simulation-organizing.py', label='Audit Simulation')

st.markdown(get_sidebar_html(), unsafe_allow_html=True)

float_init(theme=True, include_unstable_primary=False)

# ─────────────────────────────────────────────────────────────
def display_message_part(part):
    if part.part_kind == 'user-prompt':
        with st.chat_message("user"):
            st.markdown(part.content)
    elif part.part_kind == 'text':
        with st.chat_message("assistant"):
            st.markdown(part.content)

def update_document(phase:str, bewertung:str, begruendung:str, verbessung:str, methoden:str, ki_tools:str):
    new_text = get_review_heading()
    new_text += get_new_review_text(phase, bewertung, begruendung, verbessung, methoden, ki_tools)
    st.session_state.doc_text = new_text

async def run_agent_with_streaming(user_input, use_history=True, add_message=True):
    print("User input:", user_input)
    print("Use history:", use_history)

    async with chat_agent.run_stream(
        user_input,
        deps=st.session_state.agent_deps,
        message_history=st.session_state.org_chat_messages if use_history else None
    ) as result:
        async for message in result.stream_text(delta=True):
            yield message

    if add_message:
        st.session_state.org_chat_messages.extend(result.new_messages())

# ─────────────────────────────────────────────────────────────
# Init session state

default_text = get_default_hint_text()

if "agent_deps" not in st.session_state:
    with st.spinner("Initialisiere KI-Agent..."):
        st.session_state.agent_deps = get_agent()

if "org_chat_messages" not in st.session_state:
    st.session_state.org_chat_messages = []

if "o_user_response" not in st.session_state:
    st.session_state.o_user_response = []

if "o_user_inputs" not in st.session_state:
    st.session_state.o_user_inputs = []

if "o_question_index" not in st.session_state:
    st.session_state.o_question_index = 0

if "o_question_asked_once" not in st.session_state:
    st.session_state.o_question_asked_once = False

if "o_got_valid_response" not in st.session_state:
    st.session_state.o_got_valid_response = False

if "have_ux_expert" not in st.session_state:
    st.session_state.have_ux_expert = False

if "ux_experience" not in st.session_state:
    st.session_state.ux_experience = ''

if "doc_text" not in st.session_state:
    st.session_state.doc_text = default_text

if "o_evaluation_finished" not in st.session_state:
    st.session_state.o_evaluation_finished = False

# ─────────────────────────────────────────────────────────────

with st.container():
    st.markdown(get_header_html(), unsafe_allow_html=True)

    css = get_header_css()
    float_parent(css=css)

st.markdown(get_padding_html(), unsafe_allow_html=True)


col1_chatbot, col2_chatbot = st.columns([1, 1])

questions = organizing_questions

response_options = organzing_response_text_options

expert_response = organizing_response_q1[1].text

async def main():

    with col1_chatbot:
        with st.container(border=False):
            scroll_container = st.container()

            with scroll_container:
                for msg in st.session_state.org_chat_messages:
                    if isinstance(msg, (ModelRequest, ModelResponse)):
                        for part in msg.parts:
                            display_message_part(part)

            index = st.session_state.o_question_index

            if index == 0 and not st.session_state.o_question_asked_once:
                with st.chat_message("assistant"):
                    st.markdown(questions[index], unsafe_allow_html=True)
                    st.session_state.org_chat_messages.extend(
                        [ModelResponse(parts=[TextPart(content=questions[index], part_kind='text')])])
                    st.session_state.o_question_asked_once = True

            with st.container():
                user_input = st.chat_input(key='content_input', placeholder="Was möchtest du wissen?")
                button_css = float_css_helper(width="37%", bottom="0.3rem", transition=0)
                float_parent(css=button_css)

            if user_input:
                if st.session_state.o_question_index == len(questions):
                    with st.chat_message("user"):
                        st.markdown(user_input)

                    full_response = ""
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        async for message in run_agent_with_streaming(user_input):
                            full_response += message
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)

                if st.session_state.o_question_index < len(questions):
                    with st.chat_message("user"):
                        st.markdown(user_input)
                        st.session_state.o_user_inputs.append(user_input)
                        st.session_state.org_chat_messages.extend([ModelRequest(parts=[UserPromptPart(content=user_input, part_kind='user-prompt')])])
                        eingabe = AssignResponseInput(frage= questions[st.session_state.o_question_index],
                                                      nutzereingabe=user_input,
                                                      antwortoptionen=response_options[st.session_state.o_question_index])

                        result = await assign_user_input(eingabe)

                    assigned_resp = result.output.assigned_response

                    if assigned_resp is None or assigned_resp == 'None':
                        with st.chat_message("assistant"):
                            st.markdown(result.output.error_message, unsafe_allow_html=True)
                            st.session_state.org_chat_messages.extend(
                                [ModelResponse(parts=[TextPart(content=result.output.error_message, part_kind='text')])])
                            st.session_state.o_got_valid_response = False
                    else:
                        st.session_state.o_got_valid_response = True
                        if st.session_state.o_question_index != 0 and st.session_state.o_question_index != 2:
                            st.session_state.o_user_response.append(assigned_resp)
                        else:
                            if assigned_resp == 'True':
                                st.session_state.have_ux_expert = True

                            if st.session_state.o_question_index == 0:
                                st.session_state.ux_experience = assigned_resp


                    if st.session_state.o_got_valid_response:
                        if assigned_resp == expert_response:
                            st.session_state.o_question_index += 1
                            st.session_state.have_ux_expert = True
                        st.session_state.o_question_index += 1
                        index = st.session_state.o_question_index

                    if index < len(questions) and st.session_state.o_got_valid_response:
                        with st.chat_message("assistant"):
                            st.markdown(questions[index], unsafe_allow_html=True)
                            st.session_state.org_chat_messages.extend(
                                [ModelResponse(parts=[TextPart(content=questions[index], part_kind='text')])])

                    repos = st.session_state.o_user_response

                    if len(repos) + 2 == len(response_options):
                        with st.spinner("Die Bewertung wird jetzt ausgeführt das kann einige Zeit dauern."):
                            if not st.session_state.have_ux_expert:
                                st.session_state.agent_deps.condition = get_no_expert_condition()
                            st.session_state.agent_deps.explicit_search_query = get_method_search_string(Phasen.ORGANIZING.value)
                            methods = ""
                            async for message in run_agent_with_streaming(user_input=get_method_user_input(Phasen.ORGANIZING.value), use_history=False, add_message=False):
                                methods += message
                            st.session_state.agent_deps.condition = get_ai_tool_condition()
                            st.session_state.agent_deps.explicit_search_query = get_ai_tool_search_query(Phasen.ORGANIZING.value)

                            ai_tools = ""
                            async for message in run_agent_with_streaming(get_ai_tool_user_input(Phasen.ORGANIZING.value), use_history=False, add_message=False):
                                ai_tools += message

                            st.session_state.agent_deps.condition = None
                            st.session_state.agent_deps.explicit_search_query = None
                            print(methods)
                            print(ai_tools)

                            a1 = next(a for a in organizing_response_q1 if a.text == repos[0])
                            a2 = next(a for a in organizing_response_q2 if a.text == repos[1])
                            a3 = next(a for a in organizing_response_q3 if a.text == repos[2])

                            response = await evaluate_phase(
                                nutzereingabe=st.session_state.o_user_inputs,
                                antworten=BewertungEingabe(antwortoptionen=[a1, a2, a3]),
                                phase=Phasen.ORGANIZING.value,
                                ux_erfahrung=st.session_state.ux_experience,
                                methoden=methods, ki_tools=ai_tools, evaluation_metrik=organzing_rating_metrik)

                            st.session_state.org_chat_messages.extend(
                                [ModelResponse(
                                    parts=[TextPart(content=response.output.gesamtbewertungstext, part_kind='text')])])
                            st.session_state.o_user_response = []
                            update_document(Phasen.ORGANIZING.value, response.output.gesamtbewertung,
                                            response.output.gesamtbegruendung,
                                            response.output.gesamtverbesserungspotential, response.output.methoden,
                                            response.output.ki_tools)
                            st.session_state.o_evaluation_finished = True

                            with st.chat_message("assistant"):
                                st.markdown(response.output.gesamtbewertungstext, unsafe_allow_html=True)



if __name__ == "__main__":
    asyncio.run(main())


with st.container():
    st.markdown(get_review_html(st.session_state.doc_text), unsafe_allow_html=True)

with st.container():
    right_float_css = get_menu_css()

    st.markdown(
        get_tertiary_button_html(),
        unsafe_allow_html=True,
    )

    col1_info, mid, col2_info = st.columns([6,1,4])
    with col1_info:

        sub_col1, sub_col2 = st.columns([5, 1])
        with sub_col1:
            st.markdown(get_menu_heading_html(Phasen.ORGANIZING.value), unsafe_allow_html=True)
        with sub_col2:
            st.button("ℹ️", help=organizing_summary, type="tertiary")

        if st.button("Wechsle in die nächste Phase", use_container_width=True, disabled=not st.session_state.get("o_evaluation_finished", False)):
            st.switch_page("pages/simulation-understanding.py")

    with col2_info:
        st.image("pictures/ucd_process_organizing.png", use_container_width=True)

    float_parent(css=right_float_css)

with st.container():
    st.download_button(
        label="Download als HTML",
        data=get_final_review_html(st.session_state.doc_text),
        file_name="review.html",
        mime="text/html"
    )
    button_css = float_css_helper(width="37%", bottom="0.3rem", left="60%", transition=0)
    float_parent(css=button_css)