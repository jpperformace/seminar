import streamlit as st


st.set_page_config(page_title="KI-Audit-Assistent", layout="wide")

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/auditsimulation-organizing.py', label='KI-Audit')


st.switch_page("pages/start.py")