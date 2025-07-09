from dotenv import load_dotenv
import streamlit as st
import asyncio

# Import all the message part classes
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse
)

from agents.agent_loader import get_agent
from agents.rag_agent import chat_agent

load_dotenv()

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/simulation-understanding.py', label='Audit Simulation')
st.sidebar.page_link('pages/simulation-organizing-v2.py', label='Audit Simulation V2')

def display_message_part(part):
    """
    Display a single part of a message in the Streamlit UI.
    Customize how you display system prompts, user prompts,
    tool calls, tool returns, etc.
    """

    # user-prompt
    if part.part_kind == 'user-prompt':
        with st.chat_message("user"):
            st.markdown(part.content)
    # text
    elif part.part_kind == 'text':
        with st.chat_message("assistant"):
            st.markdown(part.content)


async def run_agent_with_streaming(user_input):
    print("chatbot: run_agent_with_streaming")
    print(user_input)
    print(st.session_state.messages)
    print(st.session_state.agent_deps)
    async with chat_agent.run_stream(
            user_input, deps=st.session_state.agent_deps, message_history=st.session_state.messages
    ) as result:
        print(result)
        async for message in result.stream_text(delta=True):
            yield message


    print(result.new_messages())
    # Add the new messages to the chat history (including tool calls and responses)
    st.session_state.messages.extend(result.new_messages())



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


async def main():
    st.title("Nutzerzentriert Entwickelt")

    # Initialize chat history in session state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_deps" not in st.session_state:
        with st.spinner("Initialisiere Agent..."):
            st.session_state.agent_deps = get_agent()

        # Display all messages from the conversation so far
    # Each message is either a ModelRequest or ModelResponse.
    # We iterate over their parts to decide how to display them.
    for msg in st.session_state.messages:
        print("Message: {}".format(msg))
        if isinstance(msg, ModelRequest) or isinstance(msg, ModelResponse):
            for part in msg.parts:
                display_message_part(part)

    # Chat input for the user
    user_input = st.chat_input("What do you want to know?")

    if user_input:
        # Display user prompt in the UI
        with st.chat_message("user"):
            st.markdown(user_input)

        # Display the assistant's partial response while streaming
        with st.chat_message("assistant"):
            # Create a placeholder for the streaming text
            message_placeholder = st.empty()
            full_response = ""

            # Properly consume the async generator with async for
            generator = run_agent_with_streaming(user_input)
            async for message in generator:
                full_response += message
                message_placeholder.markdown(full_response + "▌")

            # Final response without the cursor
            message_placeholder.markdown(full_response)

if __name__ == "__main__":
    asyncio.run(main())
