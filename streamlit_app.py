import streamlit as st

chatbot = st.Page("pages/chatbot.py", title="Chatbot")
start = st.Page("pages/start.py", title="Getting started")

pg = st.navigation([start, chatbot])
st.set_page_config(page_title="KI-Audit-Assistent", layout="wide")
pg.run()