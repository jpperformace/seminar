import textwrap

from dotenv import load_dotenv
from streamlit_float import *
from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart
import asyncio

from agents.agent_loader import get_agent
from agents.assign_response_agent import AssignResponseInput, assign_user_input
from agents.quantitative_rating_agent import evaluate_phase, Phasen, BewertungEingabe
from agents.rag_agent import chat_agent
from audit_ratings.response_options_understanding import understanding_question_1, understanding_question_2, \
    understanding_methods_analysis_question

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

def update_document(bewertung:str, begruendung:str, verbessung:str):
    new_text = f"""
<div style="font-size: 0.85rem;">
<strong>Phase: Verstehen </strong><br>
<ul style="margin-top: 0.5rem; padding-left: 1.2rem;">
<li><strong>Bewertung:</strong> {bewertung}</li>
<li><strong>Begründung:</strong> {begruendung}</li>
<li><strong>Verbesserungsvorschlag:</strong> {verbessung}</li>
</ul>
</div>
    """
    st.session_state.doc_text = st.session_state.doc_text + "\n" + new_text


async def run_agent_with_streaming(user_input):
    async with chat_agent.run_stream(
        user_input,
        deps=st.session_state.agent_deps,
        message_history=st.session_state.und_chat_messages
    ) as result:
        async for message in result.stream_text(delta=True):
            yield message
    st.session_state.und_chat_messages.extend(result.new_messages())

# ─────────────────────────────────────────────────────────────
# Init session state

default_text = textwrap.dedent("""
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
<span style="font-size: 1.3rem; position: relative; top: -5px;">💡</span>
<h4 style="margin: 0;">Hinweis:</h4>
</div>
<p>
An dieser Stelle wird zukünftig ein zusammenfassendes Dokument zur Einschätzung und Potenzialanalyse für das Siegel <strong>„Nutzerzentriert Entwickelt“</strong> angezeigt.
Es fasst zentrale Erkenntnisse der Analysephase, die durch die interaktive Konversation mit dem KI-Assistenten gewonnen wurden, zusammen und bietet einen Überblick über empfohlene nächste Schritte im weiteren Entwicklungsprozess.
</p>
    """)

if "agent_deps" not in st.session_state:
    with st.spinner("Initialisiere KI-Agent..."):
        st.session_state.agent_deps = get_agent()

if "und_chat_messages" not in st.session_state:
    st.session_state.und_chat_messages = []

if "user_response" not in st.session_state:
    st.session_state.user_response = []

if "u_user_inputs" not in st.session_state:
    st.session_state.u_user_inputs = []

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "question_asked_once" not in st.session_state:
    st.session_state.question_asked_once = False

if "got_valid_response" not in st.session_state:
    st.session_state.got_valid_response = False

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
                <strong>Hinweis:</strong> Bitte beantworten Sie die Fragen des KI-gestützten Assistenten so ausführlich wie möglich. 
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

questions = ['Wie oft führen Sie Nutzerforschung durch, um Ihre Zielgruppe und deren Bedürfnisse zu verstehen?',
             'Welche Methoden zur Analyse der Nutzenden wenden Sie an?',
             'Wie werden die Ergebnisse der Anwenderanalyse verwendet?']

response_options = [
    [option.text for option in understanding_question_1],
    [option.text for option in understanding_methods_analysis_question],
    [option.text for option in understanding_question_2]
]




async def main():

    with col1_chatbot:
        with st.container(border=False):
            scroll_container = st.container()

            with scroll_container:
                for msg in st.session_state.und_chat_messages:
                    if isinstance(msg, (ModelRequest, ModelResponse)):
                        for part in msg.parts:
                            display_message_part(part)

            index = st.session_state.question_index

            if index == 0 and not st.session_state.question_asked_once:
                with st.chat_message("assistant"):
                    st.markdown(questions[index], unsafe_allow_html=True)
                    st.session_state.und_chat_messages.extend(
                        [ModelResponse(parts=[TextPart(content=questions[index], part_kind='text')])])
                    st.session_state.question_asked_once = True

            with st.container():
                user_input = st.chat_input(key='content_input', placeholder="Was möchtest du wissen?")
                button_css = float_css_helper(width="37%", bottom="0.3rem", transition=0)
                float_parent(css=button_css)

            if user_input:
                if st.session_state.question_index == len(questions):
                    with st.chat_message("user"):
                        st.markdown(user_input)


                    full_response = ""
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        async for message in run_agent_with_streaming(user_input):
                            full_response += message
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)

                if st.session_state.question_index < len(questions):
                    with st.chat_message("user"):
                        st.markdown(user_input)
                        st.session_state.u_user_inputs.append(user_input)
                        st.session_state.und_chat_messages.extend([ModelRequest(parts=[UserPromptPart(content=user_input, part_kind='user-prompt')])])
                        eingabe = AssignResponseInput(frage= questions[st.session_state.question_index],
                                                      nutzereingabe=user_input,
                                                      antwortoptionen=response_options[st.session_state.question_index])

                        result = await assign_user_input(eingabe)

                    assigned_resp = result.output.assigned_response

                    if assigned_resp is None or assigned_resp == 'None':
                        with st.chat_message("assistant"):
                            st.markdown(result.output.error_message, unsafe_allow_html=True)
                            st.session_state.und_chat_messages.extend(
                                [ModelResponse(parts=[TextPart(content=result.output.error_message, part_kind='text')])])
                            st.session_state.got_valid_response = False
                    else:
                        st.session_state.got_valid_response = True
                        st.session_state.user_response.append(assigned_resp)

                    if st.session_state.got_valid_response:
                        st.session_state.question_index += 1
                        index = st.session_state.question_index

                    if index < len(questions) and st.session_state.got_valid_response:
                        with st.chat_message("assistant"):
                            st.markdown(questions[index], unsafe_allow_html=True)
                            st.session_state.und_chat_messages.extend(
                                [ModelResponse(parts=[TextPart(content=questions[index], part_kind='text')])])

                    repos = st.session_state.user_response

                    print(st.session_state.user_response)
                    print(st.session_state.have_ux_expert)

                    if len(repos) == len(response_options):
                        print(st.session_state.u_user_inputs)
                        a0 = next(a for a in understanding_question_1 if a.text == repos[0])
                        a1 = next(a for a in understanding_methods_analysis_question if a.text == repos[1])
                        a2 = next(a for a in understanding_question_2 if a.text == repos[2])

                        with st.chat_message("assistant"):
                            methods_message = f", die nicht in der Nachricht  \"{st.session_state.u_user_inputs[1]}\" enthalten sind"
                            expert_message = ""
                            if not st.session_state.have_ux_expert:
                                expert_message =' und keinen UX-Experten benötigen'
                            methods = ""
                            async for message in run_agent_with_streaming(f"Welche Methoden gibt es in der Phase Verstehen{methods_message}{expert_message}?"):
                                methods += message
                            print(methods)
                            response = await evaluate_phase(
                                methoden=methods,
                                nutzereingabe=st.session_state.u_user_inputs,
                                antworten=BewertungEingabe(antwortoptionen=[a0, a1, a2]),
                                phase=Phasen.ORGANIZING.value)
                            print(response)
                            st.markdown(response.output.gesamtbewertungstext, unsafe_allow_html=True)
                            st.session_state.und_chat_messages.extend(
                                [ModelResponse(parts=[TextPart(content=response.output.gesamtbewertungstext, part_kind='text')])])
                            st.session_state.user_response = []
                            update_document(response.output.gesamtbewertung, response.output.gesamtbegruendung, response.output.gesamtverbesserungspotential)



                print(st.session_state.question_index)


if __name__ == "__main__":
    asyncio.run(main())

with st.container():
    right_float_css = float_css_helper(
        width="38%",
        top="10rem",
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
                       <h4 style="margin: 0;">Phase: Verstehen</h4>
                   </div>
               """, unsafe_allow_html=True)
        with sub_col2:

            st.button("ℹ️",
                      help="""
                      Die Phase Verstehen beinhaltet die systematische Untersuchung von Nutzungskontext, Nutzerverhalten 
                      und Zielen. Ziel ist es, fundierte Erkenntnisse über die Bedürfnisse der Nutzer zu gewinnen, um daraus 
                      Anforderungen und Gestaltungsansätze abzuleiten.
                      """,
                      type="tertiary")



        if st.button("Wechsle in nächste Phase", use_container_width=True):
            st.switch_page("pages/simulation-understanding.py")

    with col2_info:
        st.image("pictures/ucd_process_understanding.png", use_container_width=True)

    float_parent(css=right_float_css)

with st.container():
    right_float_css = textwrap.dedent("""
        position: fixed;
        width: 38%;
        top: 50%;
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
