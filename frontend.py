import json
import os
import time
import streamlit as st
import requests

st.set_page_config(
    page_title="Botanic",  # Title displayed in the browser tab
    page_icon="💬",  # Icon displayed in the browser tab
    layout="centered",  # Options: "centered" or "wide"
    initial_sidebar_state="expanded"  # Options: "auto", "expanded", or "collapsed"
)


# ORIGIN="http://127.0.0.1:5000"
ORIGIN = os.environ["FLASK_ORIGIN"]


headers = {
    "x-api-key": "test",
    "Content-Type": "application/json"
}

def is_valid_json(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None
    


def call_llm_api(prompt:str):
    body = {
    "content": prompt,
    }
    response = requests.post(f"{ORIGIN}/chatbot/chat", headers=headers, json=body)
    return response.json()

def display_response(response:requests.Response):
    assistant_message = ""

    #error
    if( response["success"]!= True):
        assistant_message = response["error_messages"] if response["error_messages"]!= None else "An error has occured while generating a response"

    response_content = response["response"]

    #image generation
    if(is_valid_json(response_content)):
        json_response = is_valid_json(response_content)
        json_image_url = json_response["image_url"]
        json_response = json_response["response"]
        st.session_state.messages.append({"role":"assistant" , "content": json_response , "image_url":json_image_url})

        st.chat_message("assistant").markdown(json_response)
        st.image(json_image_url, caption="Generated image")

        return
        
        
    # text 
    assistant_message = response_content
    st.session_state.messages.append({"role":"assistant" , "content": assistant_message})
    st.chat_message("assistant").markdown(assistant_message)




st.title("Botanic")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages :
    st.chat_message(message["role"]).markdown(message["content"])
    if("image_url" in message):
        st.image(message["image_url"], caption="Generated image")



prompt = st.chat_input("Send a message")


if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user" , "content": prompt})

    response = call_llm_api(prompt)
    display_response(response)



    
