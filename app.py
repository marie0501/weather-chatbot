import os
import streamlit as st
import requests
import time
from src.config import CHATFLOW_CHATMESSAGE_URL, CHATFLOW_PREDICTION_URL, SESSION_ID, HEADERS

MAX_RETRIES = 5
RETRY_DELAY = 2  # Delay in seconds between retries

def query(payload):
    for attempt in range(MAX_RETRIES):
        response = requests.post(CHATFLOW_PREDICTION_URL, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result['text'] != '':  # Check if the response is not empty
                return result
            else:
                st.warning("Received an empty response, retrying...")
                time.sleep(RETRY_DELAY)  # Wait before retrying
        elif response.status_code == 500:
            st.error(f"Error: Received status code 500 - Internal Server Error.")
            print(f"Response details: {response.text}")
            return None
        else:
            st.error(f"Error: Received an unexpected status code {response.status_code}")
            print(f"Response details: {response.text}")
            return None
    
    # If all retries fail
    st.error(f"Failed to get a non-empty response after {MAX_RETRIES} attempts.")
    return None

# Retrieve chat history from the API
def get_chat_history():
    response = requests.get(CHATFLOW_CHATMESSAGE_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()  
    else:
        return [] 


# Delete chat history via the API
def delete_chat_history():
    response = requests.delete(CHATFLOW_CHATMESSAGE_URL, headers=HEADERS)
    if response.status_code == 200:
        st.success("Chat history deleted successfully.")
        st.session_state["messages"] = []
    else:
        st.error("Failed to delete chat history.")


# Custom CSS for the "Clear Chat" button
def add_clear_chat_button():
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.25em 0.5em;
        }
        div.stButton > button:first-child:hover {
            background-color: #ff3333;
            color: white;
            border: none;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.write("")  # Add vertical spacing
    if st.button("Clear Chat"):
        delete_chat_history()


# Initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []


# Load and display chat history
def load_and_display_chat_history():
    chat_history = get_chat_history()
    if chat_history:
        st.session_state["messages"] = chat_history


# Filter out empty assistant responses
def filter_messages(messages):
    filtered_messages = []
    roles = {'userMessage': 'user', 'apiMessage': 'assistant'}

    for i in range(len(messages)):
        if roles[messages[i]["role"]] == "user":
            if (i + 1 < len(messages) and 
                roles[messages[i + 1]["role"]] == "assistant" and 
                messages[i + 1]["content"].strip() != ""):
                filtered_messages.append(messages[i])
                filtered_messages.append(messages[i + 1])
            continue
    return filtered_messages


# Display chat messages
def display_chat_messages(messages):
    roles = {'userMessage': 'user', 'apiMessage': 'assistant'}
    for message in messages:
        role = roles[message["role"]]
        with st.chat_message(role):
            st.markdown(message["content"])


# Handle user input and model response
def handle_user_input():
    if prompt := st.chat_input("Type your message..."):
        with st.chat_message('user'):
            st.write(prompt)

        # Store the user's message
        st.session_state["messages"].append({"role": "user", "content": prompt})

        try:
            response = query({'question': prompt, "overrideConfig": {"sessionId": SESSION_ID}})['text']
        except Exception as e:
            print(e)
            response = "Sorry, I couldn't process that request."

        # Store and display the model's response
        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)


# Main function to run the app
def main():
    col1, col2 = st.columns([4, 1])

    # Add "Clear Chat" button
    with col2:
        add_clear_chat_button()

    # Initialize session state
    initialize_session_state()

    # Load and display chat history
    load_and_display_chat_history()

    # Filter and display messages
    filtered_messages = filter_messages(st.session_state["messages"])
    display_chat_messages(filtered_messages)

    # Handle user input
    handle_user_input()

# Run the app
if __name__ == "__main__":
    main()