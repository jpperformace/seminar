from dotenv import load_dotenv
import streamlit as st

from streamlit_float import float_parent

from audit_process.general import Phasen
from ui.css import get_title_css
from ui.html import get_final_review_html

load_dotenv()

st.set_page_config(layout="wide")

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/auditsimulation-organizing.py', label='KI-Audit: Organisieren')
st.sidebar.page_link('pages/auditsimulation-understanding.py', label='KI-Audit: Verstehen')
st.sidebar.page_link('pages/auditsimulation-designing.py', label='KI-Audit: Gestalten')
st.sidebar.page_link('pages/auditsimulation-evaluation.py', label='KI-Audit: Bewerten')
st.sidebar.page_link('pages/final_report.py', label='Finaler KI-Report')


st.markdown(get_title_css(), unsafe_allow_html=True)

st.markdown(f"""
<div class="report-container">
    <h1>KI-Report für das Siegel 
        "<span class='highlight-marker'>Nutzerzentriert Entwickelt</span>"
    </h1>

""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="
        background-color:#FFF2CC; 
        padding: 15px 20px; 
        border-radius: 8px;
        font-weight:bold;
        font-size:30px;
        color:#434343;
        ">
        Phase: {Phasen.ORGANIZING.value}
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(st.session_state.organizing_final_report)

st.markdown(
    f"""
    <div style="
        background-color:#FFF2CC; 
        padding: 15px 20px; 
        border-radius: 8px;
        font-weight:bold;
        font-size:30px;
        color:#434343;
        ">
        Phase: {Phasen.UNDERSTANDING.value}
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(st.session_state.understanding_final_report)

st.markdown(
    f"""
    <div style="
        background-color:#FFF2CC; 
        padding: 15px 20px; 
        border-radius: 8px;
        font-weight:bold;
        font-size:30px;
        color:#434343;
        ">
        Phase: {Phasen.DESIGNING.value}
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(st.session_state.designing_final_report)

st.markdown(
    f"""
    <div style="
        background-color:#FFF2CC; 
        padding: 15px 20px; 
        border-radius: 8px;
        font-weight:bold;
        font-size:30px;
        color:#434343;
        ">
        Phase: {Phasen.EVALUATION.value}
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(st.session_state.evaluation_final_report)

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

    float_parent(css="""
        position: fixed;
        top: 5rem;
        right: 5rem;
        width: 11.5rem;
        height: 2.5rem;
        z-index: 9998;
        background: white;
        border-radius: 0.75rem;
    """)

