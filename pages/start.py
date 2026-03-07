import streamlit as st

from ui.css import get_title_css

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/auditsimulation-organizing.py', label='KI-Audit')

st.markdown(get_title_css(), unsafe_allow_html=True)

st.markdown("""
<div class="report-container">
    <h1>KI-Assistent für das Siegel 
        "<span class='highlight-marker'>Nutzerzentriert Entwickelt</span>"
    </h1>

""", unsafe_allow_html=True)

st.markdown(
    """
    <p style='font-size: 1.15rem; line-height: 1.6; color: #4a4a4a;'>
    Bereiten Sie sich gezielt, effizient und interaktiv auf den Audit zur <strong>nutzerzentrierten Entwicklung</strong> vor – 
    mit unserem intelligenten RAG-basierten KI-Assistenzsystem.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# Sektion: Starten Sie jetzt
st.markdown("### Starten Sie jetzt")
st.write("Testen Sie den KI-gestützten Audit-Assistenten für mehr Klarheit, Sicherheit und Struktur auf dem Weg zur Zertifizierung.")

# Button-Layout
col1, col2, spacer_right = st.columns([1, 1, 1], gap="small")

is_ready = st.session_state.get("agent_ready", False)

st.markdown("""
<style>
    /* Die Container-Klasse für Streamlit Buttons ansprechen */
    div.stButton > button {
        width: 100%;          /* Volle Breite der Spalte */
        height: 80px;         /* Deutlich höher für den großen Inhalt */
        border-radius: 20px;   /* Schön abgerundete Ecken */

        /* Flexbox sorgt dafür, dass Icon und Text sauber zentriert sind */
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 20px;             /* Abstand zwischen Icon und Text */
    }

    /* Farbe für Button 1 (Linke Spalte) */
    [data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background-color: #FFF2CC; /* Dunkelgrün */
        color: #333;
        border: none;
    }

    /* Farbe für Button 2 (Rechte Spalte) */
    [data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background-color: #FFF2CC; /* Dunkelblau */
        color: #333;
        border: none;
    }

    /* Hover-Effekt: Etwas heller werden beim Drüberfahren */
    div.stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-3px); /* Button hebt sich leicht an */
        transition: all 0.2s ease;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    div.stButton > button > div {
        font-size: 30px !important;
        font-family: "Arial" !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with col1:
    if st.button("💬 Chat", use_container_width=True, disabled=not is_ready):
        st.switch_page("pages/chatbot.py")

with col2:
    if st.button("📝 Auditsimulation", use_container_width=True, disabled=not is_ready):
        st.switch_page("pages/auditsimulation-organizing.py")

st.divider()



# Sektion: Was bietet der Assistent (Design ohne Icons, mit dezenten Trennern)
# Sektion: Was bietet der Assistent (Kacheln in 3er-Reihe)
st.markdown("### Was bietet der Assistent?")

st.markdown(
    """
    <style>
        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr); /* Genau 3 Spalten */
            gap: 16px;
            margin-top: 20px;
        }

        /* Responsive Anpassung: Auf kleinen Screens untereinander */
        @media (max-width: 800px) {
            .grid-container {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background-color: #ffffff;
            border: 1px solid #e0e6ed;
            border-radius: 2px;
            padding: 24px;
            min-height: 140px;
            display: flex;
            flex-direction: column;
            transition: all 0.2s ease-in-out;
        }

        .card:hover {
            border-color: #00a9e0;
            background-color: #fcfdfe;
        }

        .card-title {
            color: #f7ba0b;
            font-weight: 700;
            font-size: 20px;
            margin-bottom: 8px;
            line-height: 1.2;
        }

        .card-body {
            font-size: 18px;
            line-height: 1.5;
            color: #555555;
        }
    </style>

    <div class="grid-container">
        <div class="card">
            <div class="card-title">Auditablauf</div>
            <div class="card-body">Simuliert den Ablauf auf Basis realer Anforderungen.</div>
        </div>
        <div class="card">
            <div class="card-title">Strukturierte Anleitung</div>
            <div class="card-body">Führt Sie schrittweise durch die Phasen des Prozesses.</div>
        </div>
        <div class="card">
            <div class="card-title">Ersteinschätzung</div>
            <div class="card-body">Subjektive Bewertung Ihrer aktuellen Zertifizierungsreife.</div>
        </div>
        <div class="card">
            <div class="card-title">Umfassende Erklärungen</div>
            <div class="card-body">Klärung komplexer Themen zur nutzerzentrierten Entwicklung.</div>
        </div>
        <div class="card">
            <div class="card-title">Verbesserungsvorschläge</div>
            <div class="card-body">Individuelle Optimierungstipps auf Basis Ihrer Eingaben.</div>
        </div>
        <div class="card">
            <div class="card-title">Zusammenfassung</div>
            <div class="card-body">Automatische Erfassung wichtiger Erkenntnisse im Verlauf.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# Sektion: Ergebnis
st.markdown("### Ergebnis der Auditsimulation")
st.markdown(
    """
    <p style='line-height: 1.6;'>
    Ob Grundlagenklärung, Interpretationsfragen oder Verbesserungspotenziale – der Assistent geht auf Ihre Fragen ein, 
    identifiziert Schwachstellen und bietet konstruktive Vorschläge zur Optimierung. Während des interaktiven Dialogs 
    werden zentrale Erkenntnisse automatisch erfasst und in einem übersichtlichen Dokument für Sie zusammengefasst 
    – als Basis für Ihre weitere Vorbereitung oder Teamabstimmungen.
    </p>
    """,
    unsafe_allow_html=True
)


from agents.agent_loader import get_agent

if "agent_ready" not in st.session_state:
    agent = get_agent()  # Lädt und cached
    st.session_state.agent_ready = True
    st.rerun()