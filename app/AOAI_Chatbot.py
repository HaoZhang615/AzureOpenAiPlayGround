from openai import AzureOpenAI
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Azure OpenAI Chatbot")

# Initialize session state attributes  
if "messages" not in st.session_state:  
    st.session_state.messages = []  

# Azure Open AI Configuration
api_base = os.getenv("AOAI_API_BASE") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
api_key = os.getenv("AOAI_API_KEY")
api_version = os.getenv("AOAI_API_VERSION")
client = AzureOpenAI(
    api_key=api_key,  
    api_version=api_version,
    azure_endpoint = api_base,
)

# Sidebar Configuration
with st.sidebar:
    # Temperature and token slider
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )
    Max_Token = st.sidebar.slider(
        "Max. Tokens",
        min_value=10,
        max_value=4096,
        value=256,
        step=64
    )
    # default system message
    default_system_message = "You are an helpful AI assistant."
    # make customizable system prompt
    system_prompt = st.sidebar.text_area("System Prompt", default_system_message, height=200)

    # dropdown for selecting the model with options for gpt-4, gpt-4o and gpt-4o-mini, default is gpt-4. 
    model = st.selectbox("Select Model", ["gpt-4","gpt-4o","gpt-4o-mini"], index=0)
    if model == "gpt-4":
        model = os.getenv("GPT4_MODEL_NAME")
    elif model == "gpt-4o":    
        model = os.getenv("GPT4o_MODEL_NAME")
    else:
        model = os.getenv("GPT4o_mini_MODEL_NAME")

    def clear_chat_history():
        st.session_state.messages = []
        st.session_state.chat_history = []
    if st.button("Restart Conversation :arrows_counterclockwise:"):
        clear_chat_history()
  
# Display chat history  
for message in st.session_state.messages:  
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])  

# Handle new message  
if prompt := st.chat_input("type here..."):  
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):  
        st.markdown(prompt)  
    with st.chat_message("assistant"):  
        # Define the system message
        system_message = {"role": "system", "content": system_prompt}
        
        # Prepend the system message to the list of messages
        messages = [system_message] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        stream = client.chat.completions.create(  
            model=model,  
            messages=messages,  
            stream=True,  
            temperature=temperature,  
            max_tokens=Max_Token  
        )  
        response = st.write_stream(stream)  
        st.session_state.messages.append({"role": "assistant", "content": response})
