import json
import re
from enum import Enum, auto

from dotenv import load_dotenv
import streamlit as st
import asyncio

# Import all the message part classes
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse
)

from agents.agent_loader import get_agent
from agents.retrieval_agent import chat_agent
from agents.welcome_agent import get_welcome_message, start_simulation
from audit_process.general import Phasen
from audit_process.organizing import organizing_questions


class ChatState(str, Enum):
    WELCOME = "Welcome"
    START_SIMULATION = "Start Simulation"
    FOLLOW_UP = "Follow-Up"

load_dotenv()

st.sidebar.page_link('pages/start.py', label='Getting Started')
st.sidebar.page_link('pages/chatbot.py', label='Chatbot')
st.sidebar.page_link('pages/simulation-organizing.py', label='Audit Simulation')
st.sidebar.page_link('pages/auditsimulation.py', label='KI Auditsimuation')

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

def add_response_messages_to_history(messages):
    for msg in messages:
        if isinstance(msg, ModelResponse):
            st.session_state.messages.append(msg)

async def run_welcome_agent_with_streaming():
    async with get_welcome_message(Phasen.ORGANIZING.value) as response:

        print(response)
        async for output in response.stream_output():
            yield output

    # Add the new messages to the chat history (including tool calls and responses)
    add_response_messages_to_history(response.new_messages())



async def run_simulation_agent_with_streaming(userinput, frage):
    print("Starting simulation agent")
    print(frage)
    async with start_simulation(userinput, frage, st.session_state.messages) as response:
        async for message in response.output.antworttext.stream_text(delta=True):
            yield message

    add_response_messages_to_history(response.new_messages())

async def run_retrieval_agent_with_streaming(user_input):
    async with chat_agent.run_stream(
            user_input, deps=st.session_state.agent_deps, message_history=st.session_state.messages
    ) as result:
        async for message in result.stream_text(delta=True):
            yield message

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

    if "chat_state" not in st.session_state:
        st.session_state.chat_state = ChatState.WELCOME

    if "question_counter" not in st.session_state:
        st.session_state.question_counter = 0

    if "stream_text" not in st.session_state:
        st.session_state.stream_text = True
        # Display all messages from the conversation so far
    # Each message is either a ModelRequest or ModelResponse.
    # We iterate over their parts to decide how to display them.
    for msg in st.session_state.messages:
        if isinstance(msg, ModelRequest) or isinstance(msg, ModelResponse):
            for part in msg.parts:
                display_message_part(part)

    print(st.session_state.chat_state)
    if st.session_state.chat_state == ChatState.WELCOME:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""

            async for chunk in run_welcome_agent_with_streaming():
                matches = re.findall(r'"antworttext"\s*:\s"*(.*)', chunk, re.DOTALL)
                simulation_started = re.findall(r'"simulation_gestartet"\s*:\s*(true|false)', chunk)

                if matches and not simulation_started:
                    text = matches[0]

                    if '",' in matches[0]:
                        text = text.split('",')[0]

                    if text.endswith('\\'):
                        text = text.rstrip("\\")

                    text = bytes(text, "utf-8").decode("unicode_escape")
                    text = text.encode("latin1").decode("utf-8")
                    full = text
                    placeholder.markdown(full + "▌")

            placeholder.markdown(full)
        st.session_state.chat_state = ChatState.START_SIMULATION


    # Chat input for the user
    user_input = st.chat_input("What do you want to know?")

    if user_input:
        # Display user prompt in the UI
        with st.chat_message("user"):
            st.markdown(user_input)

        # Display the assistant's partial response while streaming

        with st.chat_message("assistant"):
            # Create a placeholder for the streaming text
            print('UserInput')

            message_placeholder = st.empty()
            full_response = ""

            # Properly consume the async generator with async for
            print(st.session_state.chat_state)
            if st.session_state.chat_state == ChatState.START_SIMULATION:
                print("richtig")
                generator = run_simulation_agent_with_streaming(user_input, organizing_questions[0])
            else:
                generator = None

            async for message in generator:
                full_response += message
                message_placeholder.markdown(full_response + "▌")

            # Final response without the cursor
            message_placeholder.markdown(full_response)

if __name__ == "__main__":
    asyncio.run(main())
