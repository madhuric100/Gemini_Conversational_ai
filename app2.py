import os
from dotenv import load_dotenv
import streamlit as st 
import google.generativeai as genai
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

load_dotenv()

# Configure the API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("Google API key is not set.")

genai.configure(api_key=api_key)

# Function to start or continue chat session
def start_or_continue_chat(history):
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat()
    for message in history:
        chat.send_message(message.content)
    return chat

# Streamlit app configuration
st.set_page_config(page_title='Q&A Demo')
st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
        SystemMessage(content="You are a responseful AI assistant")
    ]

# User input and interaction
user_input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and user_input:
    chat = start_or_continue_chat(st.session_state['chat_history'])
    st.session_state['chat_history'].append(HumanMessage(content=user_input))
    response = chat.send_message(user_input)
    # st.write("Response object:", response)  # Debugging: Print response object
    if hasattr(response, 'candidates') and response.candidates:
        generated_text = response.candidates[0].content.parts[0].text
        st.session_state['chat_history'].append(AIMessage(content=generated_text))
        st.subheader("The response is")
        st.write(generated_text)
    else:
        st.write("No response received")

st.subheader("The Chat History is")

for message in st.session_state['chat_history']:
    role = "User" if isinstance(message, HumanMessage) else "System" if isinstance(message, SystemMessage) else "AI"
    st.write(f'{role}: {message.content}')
