import streamlit as st

chatbot = st.Page("pages/chatbot.py", title="Chatbot")
hello = st.Page("pages/hello.py", title="Hello World")

pg = st.navigation([hello, chatbot])
st.set_page_config(page_title="Data manager")
pg.run()