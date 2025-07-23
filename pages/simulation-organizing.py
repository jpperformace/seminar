import textwrap
from typing import Optional

from dotenv import load_dotenv
from streamlit_float import *
from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart
import asyncio

from agents.agent_loader import get_agent
from agents.assign_response_agent import AssignResponseInput, assign_user_input
from agents.quantitative_rating_agent import evaluate_phase, Phasen, BewertungEingabe
from agents.rag_agent import chat_agent
from ui.messages import get_new_review_text, get_default_hint_text, get_review_heading
from audit_ratings.response_options_organizing import organizing_question_1, organizing_question_3, organizing_question_2

load_dotenv()

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/simulation-organizing.py', label='Audit Simulation')

st.markdown(
    """
   <style>
   [data-testid="stSidebar"][aria-expanded="true"]{
       min-width: 15%;
       max-width: 15%;
   }
   """,
    unsafe_allow_html=True,
)

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

async def run_agent_with_streaming(user_input):
    async with chat_agent.run_stream(
        user_input,
        deps=st.session_state.agent_deps
    ) as result:
        async for message in result.stream_text(delta=True):
            yield message
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

# ─────────────────────────────────────────────────────────────

with st.container():
    st.markdown("""
    <div style="
        position: relative;
        width: 80%;
    ">
        <div id="sticky-header" style="
            position: sticky;
            top: 1cm;
            background-color: white;
            padding: 0.1rem;
            margin-bottom: 0.1rem;
            border-bottom: 1px solid #ccc;
            z-index: 1000;
        ">
            <h2 style="margin: 0;">KI-Assistent für Siegel „Nutzerzentriert Entwickelt“</h2>
            <p style="margin: 0;">
                Hinweis: Bitte beantworten Sie die Fragen des KI-gestützten Assistenten so ausführlich wie möglich. 
                Sollten Unsicherheiten bestehen, geben Sie diese bitte an – der Assistent kann dadurch gezielter Rückfragen stellen 
                oder weiterführende Informationen bereitstellen.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    css = float_css_helper(
        width="100%",
        top="1cm",
        transition=0,
        margin="0rem",
        additional_css="background-color: white !important; z-index: 1000;"
    )
    float_parent(css=css)

st.markdown("""
<div style="height: 20px; background-color: white;"></div>
""", unsafe_allow_html=True)


col1_chatbot, col2_chatbot = st.columns([1, 1])

questions = ['Wie würdest du den Reifegrad eurer Organisation im Bereich nutzerzentrierte Entwicklung einschätzen – von Einsteiger bis sehr erfahren?',
             'Wer übernimmt in Ihrem Unternehmen Aufgaben im Bereich Usability und User Experience (UUX)?',
             'Gibt es ein UX-Experten in Ihrem Unternehmen?',
             'Können am Entwickungsprozess des digitalen Produktes / der Dienstleistung beteiligte Mitarbeitende Usability-Qualitfikationen nachweisen?',
             'Wie ist die interne Kommunikation und Zusammenarbeit in Bezug auf "Usability und User Experience" im Entwicklungsprozess strukturiert?']

response_options_UX_experience = ['Einsteiger – Erste Berührungspunkte, keine oder sehr geringe praktische Erfahrung',
                                  'Grundkenntnisse – Einzelne UX-Methoden bekannt, punktuell angewendet',
                                  'Fortgeschritten – Regelmäßige Anwendung nutzerzentrierter Methoden im Projektkontext',
                                  'Erfahren – Systematische Integration in Prozesse, klare Zuständigkeiten',
                                  'Sehr erfahren – Strategisch verankert, teamübergreifend gelebt, kontinuierliche Optimierung']
response_options_expert = ['True', 'False']

response_options = [
    response_options_UX_experience,
    [option.text for option in organizing_question_1],
    response_options_expert,
    [option.text for option in organizing_question_2],
    [option.text for option in organizing_question_3]
]

expert_response = organizing_question_1[1].text




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
                        if not st.session_state.have_ux_expert:
                            st.session_state.agent_deps.condition = "Es gibt keine UX-Experten im Unternehmen. Wähle nur Methoden aus die keinen benötigen."

                        methods = ""
                        async for message in run_agent_with_streaming(
                                user_input=f"Welche Methoden gibt es in der Phase Organisieren?"):
                            methods += message
                        ki_tools = ""
                        async for message in run_agent_with_streaming(
                                f"Welche KI_Tools kann man in der Phase Organsieren anwenden?"):
                            ki_tools += message
                        print(methods)
                        print(ki_tools)
                        a1 = next(a for a in organizing_question_1 if a.text == repos[0])
                        a2 = next(a for a in organizing_question_2 if a.text == repos[1])
                        a3 = next(a for a in organizing_question_3 if a.text == repos[2])
                        with st.chat_message("assistant"):
                            response = await evaluate_phase(
                                nutzereingabe=st.session_state.o_user_inputs,
                                antworten=BewertungEingabe(antwortoptionen=[a1, a2, a3]),
                                phase=Phasen.ORGANIZING.value,
                                ux_erfahrung=st.session_state.ux_experience,
                                methoden=methods, ki_tools=ki_tools)

                            st.markdown(response.output.gesamtbewertungstext, unsafe_allow_html=True)
                            st.session_state.org_chat_messages.extend(
                                [ModelResponse(parts=[TextPart(content=response.output.gesamtbewertungstext, part_kind='text')])])
                            st.session_state.o_user_response = []
                            update_document(Phasen.ORGANIZING.value, response.output.gesamtbewertung,
                                            response.output.gesamtbegruendung,
                                            response.output.gesamtverbesserungspotential, response.output.methoden,
                                            response.output.ki_tools)



                print(st.session_state.o_question_index)


if __name__ == "__main__":
    asyncio.run(main())

with st.container():
    right_float_css = float_css_helper(
        width="38%",
        top="12rem",
        right="2rem",
        transition=0,
        height="25%",
        additional_css="""
            background-color: #f9f9f9;
            border-radius: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            z-index: 999;
        """
    )

    st.markdown(
        """
    <style>
    button[kind="tertiary"] {
        height: auto;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    col1_info, mid, col2_info = st.columns([6,1,4])
    with col1_info:

        sub_col1, sub_col2 = st.columns([5, 1])
        with sub_col1:
            st.markdown("""
                   <div style='font-size: 0.85rem'>
                       <h4 style="margin: 0;">Phase: Organisieren</h4>
                   </div>
               """, unsafe_allow_html=True)
        with sub_col2:

            st.button("ℹ️",
                      help="""Die Phase Organisation umfasst alle organisatorischen Elemente, die sicherstellen, 
                      dass die Benutzererfahrung eine hohe Priorität im Unternehmen hat. Dazu gehören die 
                      Verankerung einer nutzerzentrierten Denkweise und das Vorhandensein von UX-Experten.""",
                      type="tertiary")



        if st.button("Wechsle in nächste Phase", use_container_width=True):
            st.switch_page("pages/simulation-understanding.py")

    with col2_info:
        st.image("pictures/ucd_process_organizing.png", use_container_width=True)

    float_parent(css=right_float_css)

with st.container():
    right_float_css = textwrap.dedent("""
        position: fixed;
        width: 38%;
        top: 53%;
        right: 2rem;
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        z-index: 999;
        height: 40%;
        overflow-y: auto;
    """).replace("\n", " ")

    text = f"""
<div style="{right_float_css}">
<div style="font-size: 0.85rem; line-height: 1.5; color: #333;">
{st.session_state.doc_text}
</div>
</div>
    """
    st.markdown(text, unsafe_allow_html=True)
