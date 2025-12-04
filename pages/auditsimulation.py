import json
import re
from enum import Enum, auto

from docutils.nodes import Part
from dotenv import load_dotenv
import streamlit as st
import asyncio

from pydantic_ai import TextPart
# Import all the message part classes
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse, ToolCallPart, UserPromptPart
)

from agents.agent_loader import get_agent
from agents.context_agent import assign_user_input, AssignResponseInput
from agents.retrieval_agent import chat_agent
from agents.welcome_agent import get_welcome_message, start_simulation
from audit_process.general import Phasen
from audit_process.organizing import organizing_questions, organzing_response_text_options
from utils import extract_assistant_response_text_from_output


class ChatState(str, Enum):
    WELCOME = "Welcome"
    START_SIMULATION = "Start Simulation"
    GET_CONTEXT_INFO = "Get Context Info"
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
    print("store messages")
    print(st.session_state.messages)
    print(messages)
    for msg in messages:
        if isinstance(msg, ModelResponse):
            if isinstance(msg, ModelResponse):
                for part in msg.parts:
                    if isinstance(part, ToolCallPart):
                        output = part.args_as_dict()
                        response_text = output.get("antworttext", "")

                        text_part = TextPart(content=response_text)
                        print(text_part)
                        # ModelResponse mit einem Text-Part
                        model_response = ModelResponse(
                            parts=[text_part]
                        )

                        st.session_state.messages.append(model_response)
                        return
            st.session_state.messages.append(msg)
    print("history after storing")
    print(st.session_state.messages)

def store_output_information(output_string):
    try:
        output_data = json.loads(output_string)
    except json.JSONDecodeError as e:
        st.error(f"Fehler beim Parsen des Agenten-Outputs: {e}")
        return

    if st.session_state.chat_state in [ChatState.WELCOME, ChatState.START_SIMULATION]:
        st.session_state.simulation_started = output_data['simulation_gestartet']

async def run_welcome_agent_with_streaming():
    async with get_welcome_message(Phasen.ORGANIZING.value) as response:
        async for output in response.stream_output():
            yield output

    print("add new messages")
    add_response_messages_to_history(response.new_messages())



async def run_simulation_agent_with_streaming(userinput, frage):
    async with start_simulation(userinput, frage, st.session_state.messages) as response:

        async for output in response.stream_output():
            yield output

    add_response_messages_to_history(response.new_messages())

async def run_context_agent_with_streaming(userinput):
    agent_input = AssignResponseInput(
        frage=organizing_questions[st.session_state.o_question_index],
        nutzereingabe=userinput,
        antwortoptionen=organzing_response_text_options[st.session_state.o_question_index],
        naechste_frage=organizing_questions[st.session_state.o_question_index + 1]
    )

    async with assign_user_input(agent_input, st.session_state.messages) as response:
        print("response")
        print(response.stream_output())
        async for output in response.stream_output():
            print(output)
            yield output

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

    if "o_question_index" not in st.session_state:
        st.session_state.o_question_index = 0

    if "simulation_started" not in st.session_state:
        st.session_state.simulation_started = False
        # Display all messages from the conversation so far
    # Each message is either a ModelRequest or ModelResponse.
    # We iterate over their parts to decide how to display them.
    for msg in st.session_state.messages:
        if isinstance(msg, ModelRequest) or isinstance(msg, ModelResponse):
            for part in msg.parts:
                print("Parts")
                print(part)
                display_message_part(part)

    if st.session_state.chat_state == ChatState.WELCOME:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""
            output_string = ""
            stream_antworttext = True

            async for chunk in run_welcome_agent_with_streaming():
                output_string = chunk
                if stream_antworttext:
                    print(chunk)
                    full = chunk.antworttext
                    placeholder.markdown(full + "▌")

                # Stoppe das Streaming, sobald der Text abgeschlossen ist
                if '",' in chunk:
                    stream_antworttext = False

            placeholder.markdown(full)
            st.session_state.simulation_started = output_string.simulation_gestartet

        st.session_state.chat_state = ChatState.START_SIMULATION

    if st.session_state.simulation_started:
        st.session_state.chat_state = ChatState.GET_CONTEXT_INFO
    # Chat input for the user
    user_input = st.chat_input("What do you want to know?")

    if user_input:
        # Display user prompt in the UI
        with st.chat_message("user"):
            st.markdown(user_input)
            st.session_state.messages.extend(
                [ModelRequest(parts=[UserPromptPart(content=user_input)])])

        # Display the assistant's partial response while streaming

        with st.chat_message("assistant"):
            # Create a placeholder for the streaming text
            print('UserInput')

            message_placeholder = st.empty()
            full = ""
            output_string = ""
            stream_antworttext = True

            # Properly consume the async generator with async for
            print(st.session_state.chat_state)
            if st.session_state.chat_state == ChatState.START_SIMULATION:
                generator = run_simulation_agent_with_streaming(user_input, organizing_questions[0])
            elif st.session_state.chat_state == ChatState.GET_CONTEXT_INFO:
                generator = run_context_agent_with_streaming(user_input)
            else:
                raise ValueError('Invalid chat state')

            async for chunk in generator:
                output_string = chunk
                print(chunk)
                if stream_antworttext:
                    full = chunk.antworttext
                    message_placeholder.markdown(full + "▌")
                if '",' in chunk:
                    stream_antworttext = False

            message_placeholder.markdown(full)

            if st.session_state.chat_state == ChatState.START_SIMULATION:
                st.session_state.simulation_started = output_string.simulation_gestartet


if __name__ == "__main__":
    asyncio.run(main())
