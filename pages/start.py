import streamlit as st

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/simulation-organizing.py', label='Audit Simulation')

st.markdown(
    """
    <style>
        .main {
            background-color: #f7f9fb;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    ## KI-Assistent für Siegel \"Nutzerzentriert Entwickelt\"

    Bereiten Sie sich gezielt, effizient und interaktiv auf den Audit zur **nutzerzentrierten Entwicklung** vor – mit unserem intelligenten **RAG-basierten KI-Assistenzsystem**.
    
    ---
    
    ### 🚀 Starten Sie jetzt!
    
    Testen Sie den KI-gestützten Audit-Assistenten –  
    für mehr Klarheit, Sicherheit und Struktur auf dem Weg zur Zertifizierung.
    """
)

col1, col2, spacer_right = st.columns([1, 1, 2], gap="small")

with col1:
    if st.button("💬 Frage stellen", use_container_width=True,  disabled=not st.session_state.get("agent_ready", False)):
        st.switch_page("pages/chatbot.py")

with col2:
    if st.button("🖥️ Simulation starten", use_container_width=True,  disabled=not st.session_state.get("agent_ready", False)):
        st.switch_page("pages/simulation-organizing.py")

st.markdown(
    """
    ### 🎯 Was bietet der Assistent?

    - **Simuliert den Auditablauf** auf Basis realer Anforderungen  
    - **Strukturierte Anleitung** durch die Phasen des Zertifizierungsprozesses  
    - **Subjektive Ersteinschätzung** über die Zertifizierungsreife  
    - **Umfassende Erklärungen** komplexer Themen über nutzerzentriere Entwicklung– mit Möglichkeit zur Rückfrage  
    - **Individuelle Verbesserungsvorschläge** auf Basis Ihrer Eingaben  
    - **Automatische Zusammenfassung** wichtiger Erkenntnisse im Gesprächsverlauf  

    ---
    
    ### 📄 Ergebnis: Ihr individuelles Trainingsprotokoll
    
    Ob Grundlagenklärung, Interpretationsfragen oder Verbesserungspotenziale – der Assistent geht auf Ihre Fragen ein, identifiziert Schwachstellen und bietet konstruktive Vorschläge zur Optimierung. Während des interaktiven Dialogs werden zentrale Erkenntnisse automatisch erfasst und in einem übersichtlichen Dokument für Sie zusammengefasst – als Basis für Ihre weitere Vorbereitung oder Teamabstimmungen.
    """
)

from agents.agent_loader import get_agent

if "agent_ready" not in st.session_state:
    agent = get_agent()  # Lädt und cached
    st.session_state.agent_ready = True
    st.rerun()