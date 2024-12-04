import streamlit as st
from src.flowise import get_chat_history_flowise, delete_chat_history, query
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_delete_chat_history():
    session_id = st.session_state.get("session")
    logging.info(f"Attempting to delete chat history for session: {session_id}")

    data = delete_chat_history(session_id)
    logging.debug(f"Response from delete_chat_history: {data}")

    if data:
        logging.info(f"Chat history deleted successfully for session: {session_id}")
        return data
    else:
        logging.error("Failed to delete chat history.")
        st.error("Failed to delete chat history.")
        return None


def get_chat_history():
    session_id = st.session_state.get("session")
    logging.info(f"Retrieving chat history for session: {session_id}")

    data, status = get_chat_history_flowise(session_id)
    logging.info(f"Response from chat_history: {data}")

    if status:
        logging.info(f"Chat history retrieved successfully for session: {session_id}")
        return data
    else:
        logging.error(f"Failed to retrieve chat history for session: {session_id}")
        st.error(f"Failed to retrieve chat history. {session_id}")
        return []


def query_chatbot(question):
    session_id = st.session_state.get("session")
    logging.info(f"Querying chatbot with question: '{question}' for session: {session_id}")

    data = query(question, session_id)
    logging.debug(f"Response from query: {data}")

    if data:
        logging.info(f"Received response from chatbot for session: {session_id} and data {data}")
        return data
    else:
        logging.error("Failed to get chatbot response.")
        st.error("Failed to get chatbot response.")
        return None


# Functions for Streamlit Interface

def add_clear_chat_button():
    """
    Adds a custom "Clear Chat" button to the Streamlit interface, with custom CSS styling.
    """
    
    # st.markdown("""
    #     <style>
    #     div.stButton > button:first-child {
    #         background-color: #ff4b4b;
    #         color: white;
    #         border: none;
    #         border-radius: 5px;
    #         padding: 0.25em 0.5em;
    #     }
    #     div.stButton > button:first-child:hover {
    #         background-color: #ff3333;
    #         color: white;
    #         border: none;
    #         border-radius: 5px;
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)

    #st.write("")  # Add vertical spacing
    if st.button("Clear Chat"):
        get_delete_chat_history()
        st.session_state["messages"] = []  # Clear messages in session


def initialize_session_state():
    """
    Initializes the session state for storing chat messages if it hasn't been initialized.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = []


def load_and_display_chat_history():
    """
    Loads chat history from the API and stores it in the session state.
    """
    chat_history = get_chat_history()
    if chat_history:
        st.session_state["messages"] = chat_history


def filter_messages(messages):
    """
    Filters the messages to only include user and non-empty assistant responses.
    
    Args:
        messages (list): A list of messages with roles and content.
        
    Returns:
        list: A filtered list of user-assistant message pairs.
    """
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


def display_chat_messages(messages):
    """
    Displays the filtered chat messages in the Streamlit chat interface.
    
    Args:
        messages (list): A list of messages with roles and content.
    """
    roles = {'userMessage': 'user', 'apiMessage': 'assistant'}
    for message in messages:
        role = roles[message["role"]]
        with st.chat_message(role):
            st.markdown(message["content"])


def handle_user_input():
    """
    Handles user input from the chat interface, sends the query to the API, and displays the response.
    """
    if prompt := st.chat_input("Type your message..."):
        logging.info(f"User input: {prompt}")

        with st.chat_message('user'):
            st.write(prompt)

        # Store the user's message
        st.session_state["messages"].append({"role": "user", "content": prompt})
        logging.info(f"Stored user message in session state: {prompt}")

        response = ''

        try:
            # Query the chatbot API
            response = query_chatbot(prompt)
            logging.info(f"Received response from chatbot: {response}")

            if response:
                st.session_state["messages"].append(response)
                logging.info(f"Stored chatbot response in session state: {response['content']}")
            else:
                logging.warning(f"No response received from chatbot for prompt: {prompt}")
        except Exception as e:
            # Log the exception
            logging.error(f"Error querying chatbot: {str(e)}")
            st.session_state["messages"].append({"role": "assistant", "content": "Sorry, I couldn't process that request."})

        # Display the assistant's response
        if response:
            with st.chat_message("assistant"):
                st.write(response)
                logging.info(f"Displayed assistant response: {response}")
        else:
            logging.warning(f"Assistant response not displayed as response is None")



def show_chat_interface():
    """
    This function handles displaying the chat interface once the user is authenticated.
    """
    _, col2, col3 = st.columns([4, 1, 1])

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


def main():
   st.session_state["session"] = 'weather'
   show_chat_interface()

# Run the app
if __name__ == "__main__":
    main()
