import streamlit as st

st.set_page_config(page_title="KI-Audit-Assistent", layout="wide")

start = st.Page("pages/start.py", title="Getting Started")
chatbot = st.Page("pages/chatbot.py", title="Chatbot")
simulation = st.Page("pages/organizing.py", title="Audit Simulation")

pg = st.navigation([start, chatbot, simulation])

pg.run()

