import os
import json
import streamlit as st
import base64
from groq import Groq

# Streamlit page configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="MEDICINE",
    page_icon="⚕️",
    layout="wide"
)

# Function to encode image to Base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Path to your local image
image_path = "jungle.jpg"

# Convert image to Base64
base64_image = get_base64_image(image_path)

# back
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# API Key inntegration
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Initialize chat sessions in session state
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# Sidebar navigation
st.sidebar.title("💬 Chat Sessions")
selected_chat = st.sidebar.radio("Select a chat", list(st.session_state.chat_sessions.keys()))

# Button to start a new chat
if st.sidebar.button("➕ New Chat"):
    new_chat_name = f"Chat {len(st.session_state.chat_sessions)}"
    st.session_state.chat_sessions[new_chat_name] = []
    st.session_state.current_chat = new_chat_name
    st.rerun()

st.session_state.current_chat = selected_chat

#  page title
st.title("👨‍⚕️ Ayurveda GPT 2.O")
st.subheader("KRITIKA, RAJESH, AAKASH, RAJESH")
st.sidebar.success("Select a page above.")

#chat history display 
chat_history = st.session_state.chat_sessions[st.session_state.current_chat]
for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message:
user_prompt = st.chat_input("HOW CAN I HELP YOU 😊 ...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    chat_history.append({"role": "user", "content": user_prompt})

    # user will send message to llm to get a repsonse
    messages = [
        {"role": "system", "content": "You are a medical guide in Ayurveda "},
        *chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_response})

    # Display of LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
