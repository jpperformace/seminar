from dotenv import load_dotenv
from streamlit_float import *
from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart
import asyncio

from agents.agent_loader import get_agent
from agents.quantitative_rating_agent import evaluate_phase, BewertungEingabe, Phasen
from agents.rag_agent import chat_agent
from audit_ratings.reponse_options_organizing import organizing_question_1, organizing_question_2, \
    organizing_question_3, organizing_question_4

load_dotenv()

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/simulation-organizing.py', label='Audit Simulation')
st.sidebar.page_link('pages/simulation-organizing-v2.py', label='Audit Simulation V2')

float_init(theme=True, include_unstable_primary=False)


# ─────────────────────────────────────────────────────────────
def display_message_part(part):
    if part.part_kind == 'user-prompt':
        with st.chat_message("user"):
            st.markdown(part.content)
    elif part.part_kind == 'text':
        with st.chat_message("assistant"):
            st.markdown(part.content)

async def run_agent_with_streaming(user_input):
    async with chat_agent.run_stream(
        user_input,
        deps=st.session_state.agent_deps,
        message_history=st.session_state.o_messages
    ) as result:
        async for message in result.stream_text(delta=True):
            yield message
    st.session_state.o_messages.extend(result.new_messages())

# ─────────────────────────────────────────────────────────────
# Init session state

if "contents" not in st.session_state:
    st.session_state.contents = []

if "o_messages" not in st.session_state:
    st.session_state.o_messages = []

if "agent_deps" not in st.session_state:
    with st.spinner("Initialisiere KI-Agent..."):
        st.session_state.agent_deps = get_agent()

# ─────────────────────────────────────────────────────────────

with st.container():
    st.markdown("""
    <div style="
        position: relative;
        width: 100%;
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
                Bereiten Sie sich gezielt, effizient und interaktiv auf den Audit zur
                <strong>nutzerzentrierten Entwicklung</strong> vor – mit unserem intelligenten
                <strong>RAG-basierten KI-Assistenzsystem</strong>.
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

with st.container():
    col1_context, col2_context = st.columns([1, 1])

    with col1_context:
        st.markdown("""
        <div style="height: 10px; background-color: white;"></div>
        """, unsafe_allow_html=True)

        organizing_box1 = st.selectbox(
            "Wer übernimmt in Ihrem Unternehmen Aufgaben im Bereich Usability und User Experience (UUX)?",
            ("Es gibt ein ganzes UUX-Team oder eine UUX-Abteilung.", "Es gibt einen UUX-Experten.",
             "Andere Mitarbeitende (z.B. Software-Developer, Projektleitung, Produktmanagement).",
             "Bisher gibt es hierfür niemand Dezidiertes.")
        )

        organizing_box2 = st.selectbox(
            "Können am Entwickungsprozess beteiligte Mitarbeitende Usability-Qualitfikationen nachweisen??",
            ("Ja, alle", "Einige", "Nein")
        )

        organizing_box3 = st.selectbox(
            "Wie ist die interne Kommunikation und Zusammenarbeit in Bezug auf UUX im Entwicklungsprozess strukturiert?",
            ("Es gibt regelmäßige Meetings ausschließlich zu UUX-Themen mit allen Beteiligten.",
             "UUX ist ein fester Tagesordnungspunkt in regulären Projektmeetings.",
             "Die Kommunikation zu UUX findet unregelmäßig und ad hoc statt.",
             "Es gibt keine spezifische Kommunikation zu UUX.")
        )

        organizing_box4 = st.selectbox(
            "Wie ist die interne Kommunikation und Zusammenarbeit in Bezug auf UUX im Entwicklungsprozess strukturiert?",
            ("Es gibt eine verbindliche und dokumentierte Planung, wie und wann Nutzer systematisch in mehreren Projektphasen einbezogen werden (z.B. Anforderungsanalyse, Tests, Evaluation).",
             "Es ist eine Einbindung vorgesehen (z.B. Tests oder Interviews), aber nicht verbindlich dokumentiert oder nicht für alle Phasen geplant.",
             "Eine gelegentliche Einbindung ist angedacht oder erfolgt erfahrungsgemäß, aber ohne klare Planung.",
             "Es gibt keine vorgesehene Planung zur Einbindung von Nutzer.")
        )

        if st.button("Bewerten"):
            print(organizing_box1)
            a1 = next(a for a in organizing_question_1 if a.text == organizing_box1)
            a2 = next(a for a in organizing_question_2 if a.text == organizing_box2)
            a3 = next(a for a in organizing_question_3 if a.text == organizing_box3)
            a4 = next(a for a in organizing_question_4 if a.text == organizing_box4)

            with st.chat_message("assistant"):
                response = asyncio.run(evaluate_phase(BewertungEingabe(antwort1=a1, antwort2=a2, antwort3=a3, antwort4=a4), phase=Phasen.ORGANIZING.value))
                st.session_state.o_messages.extend(
                    [ModelResponse(parts=[TextPart(content=response.output, part_kind='text')])])


with st.container():
    right_float_css = float_css_helper(
        width="38%",
        top="10rem",
        right="2rem",
        transition=0,
        additional_css="""
            background-color: #f9f9f9;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            z-index: 999;
            height: 30%;
        """
    )

    with st.container():
        col1_info, col2_info = st.columns([1, 1])
        with col1_info:
            st.markdown("""
            <div style='font-size: 0.85rem'>
            <h4 style="margin: 0;">Phase: Organisieren</h4>
            Die Phase Organisation umfasst alle organisatorischen Elemente, die sicherstellen, dass die Kunden- und
            Benutzererfahrung eine hohe Priorität im Unternehmen hat. Dazu gehören die Verankerung einer agilen
            Denkweise, die Zuweisung geeigneter Budgets und das Vorhandensein engagierter UX-Experten.
            </div>
            """, unsafe_allow_html=True)
            st.markdown(
                """
                <div style="height:0.1rem; background-color:white; width:100%;"></div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Wechsle in nächste Phase", use_container_width=True):
                st.switch_page("pages/simulation-understanding.py")
        with col2_info:
            st.image("pictures/ucd_process_organizing.png", use_container_width=True)

        # Float für den gesamten Block
        float_parent(css=right_float_css)

with st.container():
    right_float_css = """
        position: fixed;
        width: 38%;
        top: 30rem;
        right: 2rem;
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        z-index: 999;
        height: 45%;
        overflow-y: auto;
    """

    st.markdown(f"""
    <div style="{right_float_css}">
        <div style="font-size: 0.85rem; line-height: 1.5; color: #333;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
              <span style="font-size: 1.3rem; position: relative; top: -5px;">💡</span>
              <h4 style="margin: 0;">Hinweis:</h4>
            </div>
            <p>
                An dieser Stelle wird zukünftig ein zusammenfassendes Dokument zur Einschätzung und Potenzialanalyse für das Siegel <strong>„Nutzerzentriert Entwickelt“</strong> angezeigt.
                Es fasst zentrale Erkenntnisse der Analysephase, die durch die interaktive Konversation mit dem KI-Assistenten gewonnen wurden, zusammen und bietet einen Überblick über empfohlene nächste Schritte im weiteren Entwicklungsprozess.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

col1_chatbot, col2_chatbot = st.columns([1, 1])


async def main():

    with col1_chatbot:

        with st.container(border=False):
            scroll_container = st.container()
            with scroll_container:
                for msg in st.session_state.o_messages:
                    if isinstance(msg, (ModelRequest, ModelResponse)):
                        for part in msg.parts:
                            display_message_part(part)
            with st.container():
                user_input = st.chat_input(key='content_input', placeholder="Was möchtest du wissen?")
                button_css = float_css_helper(width="37%", bottom="0.3rem", transition=0)
                float_parent(css=button_css)

            if user_input:
                with st.chat_message("user"):
                    st.markdown(user_input)

                full_response = ""
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    async for message in run_agent_with_streaming(user_input):
                        full_response += message
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)


if __name__ == "__main__":
    asyncio.run(main())