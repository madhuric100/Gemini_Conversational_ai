from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os
import google.generativeai as genai
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load gemini pro model and get response

def start_or_continue_chat(history):
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history)
    return chat




st.set_page_config(page_title='Q&A Demo')
st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[
        SystemMessage(content="Yor are a comedian AI assistant")
        
    ]


def get_gemini_response(chat,question):
    st.session_state['chat_history'].append(HumanMessage(content=question))
    # answer=chat(st.session_state['chat_history'])
    answer =chat.send_message(question,stream=True)
    st.session_state['chat_history'].append(AIMessage(content=answer.content))
    return answer.content
    # return response

    
user_input=st.text_input("Input:",key="input")
submit=st.button("Ask the question")
if submit and user_input:
    chat = start_or_continue_chat(st.session_state['chat_history'])
    response=get_gemini_response(chat,user_input)
    ##add user query and response to session chat history
    # st.session_state['chat_history'].append({"role": "user", "text": user_input})
    st.subheader("The response is")
    st.write("response")
    # full_response=""
    # for chunk in response:
    #     st.write(chunk.text)
    #     full_response+= chunk.text
    # st.session_state['chat_history'].append({"role": "model", "text": full_response})
    
    

st.subheader("The Chat History is")

for message in st.session_state['chat_history']:
    role = "User" if isinstance(message, HumanMessage) else "System" if isinstance(message, SystemMessage) else "AI"
    st.write(f'{role}: {message.content}') 






