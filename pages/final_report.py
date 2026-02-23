import json
import re
from enum import Enum, auto

from docutils.nodes import Part
from dotenv import load_dotenv
import streamlit as st
import asyncio

load_dotenv()

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/auditsimulation-organizing.py', label='KI-Audit: Organisieren')
st.sidebar.page_link('pages/auditsimulation-understanding.py', label='KI-Audit: Verstehen')
st.sidebar.page_link('pages/auditsimulation-designing.py', label='KI-Audit: Gestalten')
st.sidebar.page_link('pages/auditsimulation-evaluation.py', label='KI-Audit: Bewerten')
st.sidebar.page_link('pages/final_report.py', label='KI-Report')


st.title("KI-Report für Siegel Nutzerzentriert Entwickelt")

full_report = f"""

{st.session_state.organizing_final_report}

{st.session_state.understanding_final_report}

{st.session_state.designing_final_report}

{st.session_state.evaluation_final_report}
"""

# Anzeigen
st.markdown(full_report)

with st.container():
    st.download_button(
        label="⬇️ Download als HTML",
        data=get_final_review_html(
            st.session_state.get("organizing_final_report"),
            st.session_state.get("understanding_final_report"),
            st.session_state.get("evaluation_final_report"),
            st.session_state.get("evaluation_final_report")
        ),
        file_name="audit_report_document.html",
        mime="text/html"
    )

    # WICHTIG: fixed + z-index + background, damit er wirklich "immer oben" bleibt
    float_parent(css="""
        position: fixed;
        top: 5rem;
        right: 20.5rem;
        width: 11.5rem;
        height: 2.5rem;
        z-index: 9998;
        background: white;
        border-radius: 0.75rem;
    """)

