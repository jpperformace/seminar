from dotenv import load_dotenv
from streamlit_float import *
from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart
import asyncio

from agents.agent_loader import get_agent
from agents.rag_agent import chat_agent

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

questions = ['Wer übernimmt in Ihrem Unternehmen Aufgaben im Bereich Usability und User Experience (UUX)?',
             'Können am Entwickungsprozess des digitalen Produtkes / der Dienstleistung beteiligte Mitarbeitende Usability-Qualitfikationen nachweisen?',
             'Wie ist die interne Kommunikation und Zusammenarbeit in Bezug auf "Usability und User Experience" im Entwicklungsprozess strukturiert?',
             'In welchem Umfang ist die Einbindung von Nutzer im Entwicklungsprozess geplant?']

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "question_asked_once" not in st.session_state:
    st.session_state.question_asked_once = False

async def main():

    with col1_chatbot:
        index = st.session_state.question_index

        with st.container(border=False):
            scroll_container = st.container()

            print("beginning")
            print(st.session_state.o_messages)

            with scroll_container:
                for msg in st.session_state.o_messages:
                    if isinstance(msg, (ModelRequest, ModelResponse)):
                        for part in msg.parts:
                            display_message_part(part)

            if index == 0 and not st.session_state.question_asked_once:
                with st.chat_message("assistant"):
                    st.markdown(questions[index], unsafe_allow_html=True)
                    print("assitent")
                    st.session_state.o_messages.extend(
                        [ModelResponse(parts=[TextPart(content=questions[index], part_kind='text')])])
                    st.session_state.question_asked_once = True

            print("messages")



            with st.container():
                user_input = st.chat_input(key='content_input', placeholder="Was möchtest du wissen?")
                button_css = float_css_helper(width="37%", bottom="0.3rem", transition=0)
                float_parent(css=button_css)

            print('Index: ', index)

            if user_input:
                print('if user input')
                if st.session_state.question_index <= len(questions):
                    with st.chat_message("user"):
                        st.markdown(user_input)
                        st.session_state.question_index += 1
                        index = st.session_state.question_index
                        st.session_state.o_messages.extend([ModelRequest(parts=[UserPromptPart(content=user_input, part_kind='user-prompt')])])

                    print(st.session_state.o_messages)

                    if index < len(questions):
                        with st.chat_message("assistant"):
                            st.markdown(questions[index], unsafe_allow_html=True)
                            st.session_state.o_messages.extend(
                                [ModelResponse(parts=[TextPart(content=questions[index], part_kind='text')])])

                print(st.session_state.question_index)



                if st.session_state.question_index > len(questions):
                    # optional Aufzeichnung
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