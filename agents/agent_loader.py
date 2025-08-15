from agents.retrieval_agent import RAGDeps
from utils import get_chroma_client
import streamlit as st

@st.cache_resource
def load_agent():
    return RAGDeps(
        chroma_client=get_chroma_client("./chroma_db"),
        collection_name="docs",
        embedding_model="all-MiniLM-L6-v2"
    )


_agent_instance = None

def get_agent():
    global _agent_instance

    if _agent_instance is None:
        _agent_instance = load_agent()
    return _agent_instance