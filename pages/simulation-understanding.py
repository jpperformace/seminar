from dotenv import load_dotenv
from streamlit_float import *
from pydantic_ai.messages import ModelRequest, ModelResponse
import asyncio

from agents.agent_loader import get_agent
from agents.rag_agent import chat_agent

load_dotenv()

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/simulation-organizing.py', label='Audit Simulation')

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

float_init(theme=True, include_unstable_primary=False)

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
            padding: 2rem;
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
        top="1cm",  # auch hier anpassen, falls du float_parent weiterhin nutzt
        transition=0,
        additional_css="background-color: white !important; z-index: 1000;"
    )
    float_parent(css=css)

float_init(theme=True, include_unstable_primary=False)

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
            padding: 2rem;
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
        top="1cm",  # auch hier anpassen, falls du float_parent weiterhin nutzt
        transition=0,
        additional_css="background-color: white !important; z-index: 1000;"
    )
    float_parent(css=css)

with st.container():
    right_float_css = float_css_helper(
        width="42rem",
        top="13.5rem",
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
            <strong style='font-size: 1rem'>Phase: Verstehen</strong><br><br>
            Die Verstehensphase beinhaltet die systematische Untersuchung von Nutzungskontext, Nutzerverhalten
            und Zielen. Ziel ist es, fundierte Erkenntnisse über die Bedürfnisse der Nutzer zu gewinnen, um daraus
            Anforderungen und Gestaltungsansätze abzuleiten.
            </div>
            """, unsafe_allow_html=True)
            st.markdown(
                """
                <div style="height:0.1rem; background-color:white; width:100%;"></div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Wechsle in nächste Phase", use_container_width=True):
                st.switch_page("pages/simulation/designing.py")
        with col2_info:
            st.image("pictures/ucd_process_understanding.png", use_container_width=True)

        # Float für den gesamten Block
        float_parent(css=right_float_css)

with st.container():
    right_float_css = """
        position: fixed;
        width: 42rem;
        top: 33rem;
        right: 2rem;
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        z-index: 999;
        height: 40%;
        overflow-y: auto;
    """

    st.markdown(f"""
    <div style="{right_float_css}">
        <div style="font-size: 0.85rem; line-height: 1.5; color: #333;">
            <h4 style="margin-top: 0;">Einschätzung und Potenzialanalyse für das Siegel „Nutzerzentriert Entwickelt“</h4>
            <p>
                In der Phase <strong>Organisieren</strong> geht es darum, strukturelle und kulturelle Rahmenbedingungen zu schaffen,
                die eine nutzerzentrierte Entwicklung dauerhaft im Unternehmen verankern. Erste Schritte wie die Bereitstellung von
                UX-Ressourcen oder die Einbindung von UX-Zielen in die Produktstrategie sind häufig bereits erfolgt. Dennoch zeigt
                sich in vielen Fällen Optimierungspotenzial im Hinblick auf Priorisierung, Zuständigkeiten und interne Prozesse.
                Die folgenden Methoden unterstützen dabei, UX organisatorisch breiter aufzustellen und nachhaltiger in der
                Unternehmenskultur zu verankern:
            </p>
            <p>
                Diese Methode hilft dabei, den aktuellen Stand der UX-Verankerung im Unternehmen systematisch einzuschätzen.
                Durch die Analyse verschiedener Dimensionen wie Strategie, Ressourcen, Prozesse und Kultur lassen sich gezielte
                Maßnahmen ableiten, um UX organisatorisch weiterzuentwickeln.
            </p>
            <p>
                Ein praxisnahes Tool zur Klärung von Rollen, Verantwortlichkeiten und Entscheidungswegen im UX-Bereich.
                Es fördert die transparente Abstimmung zwischen UX-, Produkt- und Entwicklungsteams und hilft dabei,
                organisatorische Lücken sichtbar zu machen.
            </p>
            <p>
                Durch die Visualisierung relevanter Stakeholder wird deutlich, welche Personen oder Abteilungen Einfluss
                auf UX-Prozesse haben. So kann gezielter daran gearbeitet werden, UX strategisch und bereichsübergreifend zu verankern.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


col1, col2 = st.columns([1, 1])

async def main():

    with col1:
        with st.container(border=False):
            scroll_container = st.container()
            with scroll_container:
                for msg in st.session_state.o_messages:
                    if isinstance(msg, (ModelRequest, ModelResponse)):
                        for part in msg.parts:
                            display_message_part(part)
            with st.container():
                user_input = st.chat_input(key='content_input', placeholder="Was möchtest du wissen?")
                button_css = float_css_helper(width="45rem", bottom="0.3rem", transition=0)
                float_parent(css=button_css)

            if user_input:
                st.session_state.contents.append(user_input)  # optional Aufzeichnung
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