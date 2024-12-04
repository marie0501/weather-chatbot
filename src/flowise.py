import requests
import time
import json
import logging
from pathlib import Path
from .config import CHATFLOW_CHATMESSAGE_URL, CHATFLOW_PREDICTION_URL, CHATFLOW_URL, CHATFLOW_TOOLS_URL, OPENAI_API_KEY, HEADERS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_RETRIES = 5
RETRY_DELAY = 2  # Delay in seconds between retries

def load_data(file_path):
    try:
        logging.info("Loading data from JSON file...")
        with open(file_path, 'r') as file:
            data = json.load(file)
        logging.info("Data loaded successfully.")
        return data
    except Exception as e:
        logging.error(f"Error loading JSON: {e}")
        raise e


def create_chatflow_on_flowise(flow_data_path):

    logging.info(f"Flowise data: {flow_data_path.read_text(),}")

    payload = {
        "name": "weather-chatflow",
        "apikeyid":"9f76a8d784a95e05b2ba778b204091fe",
        "deployed": False,
        "isPublic": False,
        "flowData": flow_data_path.read_text(),
        "type": "CHATFLOW"
    }

    try:
        logging.info("Creating chatflow on Flowise...")
        response = requests.post(CHATFLOW_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        logging.info("Chatflow created successfully.")
    except requests.exceptions.RequestException as err:
        logging.error(f"Error during chatflow creation: {err}")
        raise err


def retrieve_chatflow_id():
    try:
        # Make a request to get all chatflows
        response = requests.get(CHATFLOW_URL, headers=HEADERS)
        response.raise_for_status()
        
        chatflows = response.json()
        
        if chatflows:
            # If a chatflow exists, return the last created one (or use filtering logic as needed)
            last_chatflow = chatflows[-1]
            logging.info(f"Found chatflow: {last_chatflow['name']} with ID: {last_chatflow['id']}")
            return last_chatflow['id']
        
        # If no chatflows are found, return None
        return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving chatflows: {str(e)}")
        return None

def get_all_tools():
    """
    Fetches all available tools from Flowise.
    """
    try:
        logging.info("Fetching all tools from Flowise...")
        response = requests.get(CHATFLOW_TOOLS_URL, headers=HEADERS)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4XX/5XX)
        
        tools = response.json()
        logging.info(f"Successfully retrieved {len(tools)} tools.")
        return tools

    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong with the request: {err}")
    
    return None

def create_tool(payload):
    """
    Creates a custom tool in Flowise with the provided parameters.
    
    """
    
    try:
        logging.info(f"Creating tool: {payload['name']}")
        response = requests.post(CHATFLOW_TOOLS_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4XX/5XX)
        logging.info(f"Tool '{payload['name']}' created successfully.")
        return response.json()  # Return the response data
    
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong with the request: {err}")
    
    return None


def create_chatflow():
    # Step 1: Check if any chatflow exists
    chatflow_id = retrieve_chatflow_id()
    
    if chatflow_id:
        logging.info(f"Existing chatflow found with ID: {chatflow_id}. Using existing chatflow.")
    else:
        logging.info("No existing chatflow found. Creating a new chatflow.")
        
        # Load chatflow data and create a new one
        create_chatflow_on_flowise(Path('data/weather-chatflow-no-historical-Chatflow.json'))
        
        # Retrieve the new chatflow ID after creation
        chatflow_id = retrieve_chatflow_id()
        if chatflow_id is None:
            error_msg = "CHATFLOW_ID is None. Stopping execution."
            logging.error(error_msg)
            raise Exception(error_msg)
        logging.info(f"New chatflow created with ID: {chatflow_id}.")

    # Step 2: Check if the required tools exist
    existing_tools = get_all_tools()
    required_tools = ['get_current_date', 'get_location_current_weather', 'get_location_weather_forecast']
    
    missing_tools = [tool for tool in required_tools if tool not in existing_tools]
    
    if not missing_tools:
        logging.info(f"All required tools already exist: {required_tools}")
    else:
        logging.info(f"Creating missing tools: {missing_tools}")
        
        # Load and create the missing tools
        if 'get_current_date' in missing_tools:
            custom_tool_data_0 = load_data('data/get_current_date-CustomTool.json')
            create_tool(custom_tool_data_0)

        if 'get_location_current_weather' in missing_tools:
            custom_tool_data_1 = load_data('data/get_location_current_weather-CustomTool.json')
            create_tool(custom_tool_data_1)

        if 'get_location_weather_forecast' in missing_tools:
            custom_tool_data_2 = load_data('data/get_location_weather_forecast-CustomTool.json')
            create_tool(custom_tool_data_2)

    return chatflow_id


def query(question, session_id):
    """
    Sends a query request to the chatbot with session ID and retries in case of failure.
    """

    CHATFLOW_ID = create_chatflow()

    logging.info(f"CHATFLOW_ID: {CHATFLOW_ID}")

    body_data = {
        "question": question,
        "overrideConfig": {
            "openAIApiKey": OPENAI_API_KEY,
            "sessionId": session_id,
        },
    }

    logging.info(f"Querying chatbot with session ID: {session_id} and question: {question} and body data: {body_data}")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Attempt {attempt} to query the chatbot {CHATFLOW_PREDICTION_URL + CHATFLOW_ID} with question {question}...")
            response = requests.post(CHATFLOW_PREDICTION_URL + CHATFLOW_ID, headers=HEADERS, json=body_data)

            # Check if the response is successful (status code 200)
            if response.status_code == 200:
                result = response.json()
                logging.info(f"Received response: {result}")

                # Check if the response text is non-empty
                if result.get('text', '') != '':
                    logging.info(f"Valid response received: {result['text']}")
                    return result['text']
                else:
                    logging.warning(f"Received empty response, retrying after {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)  # Wait before retrying

            # If server error (status code 500)
            elif response.status_code == 500:
                logging.error(f"Internal Server Error (500). Response details: {response.text}")
                return None

            # Handle other unexpected status codes
            else:
                logging.error(f"Unexpected status code {response.status_code}. Response details: {response.text}")
                return None

        except requests.RequestException as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    # If all retries fail
    logging.error(f"Failed to get a valid response after {MAX_RETRIES} attempts.")
    return None

def get_chat_history_flowise(session_id):
    """
    Retrieves the chat history from the chatbot API.
    
    Returns:
        list: A list of chat messages (empty list if the request fails).
    """

    CHATFLOW_ID = create_chatflow()

    logging.info(f"Fetching chat history for session ID: {session_id} and chatflow ID: {CHATFLOW_ID}")

    try:
        response = requests.get(CHATFLOW_CHATMESSAGE_URL(CHATFLOW_ID, session_id), headers=HEADERS)

        if response.status_code == 200:
            chat_history = response.json()
            logging.info(f"Chat history retrieved successfully")
            return chat_history, True
        else:
            logging.error(f"Failed to retrieve chat history. Status code: {response.status_code}, Response: {response.text}")
            return [], False
    except requests.RequestException as e:
        logging.error(f"Error while fetching chat history: {str(e)}")
        return [], False


def delete_chat_history(session_id):
    """
    Deletes the chat history via a DELETE request to the chatbot API.
    """
    CHATFLOW_ID = create_chatflow()

    logging.info(f"Deleting chat history for session ID: {session_id} and chatflow ID: {CHATFLOW_ID}")

    try:
        response = requests.delete(CHATFLOW_CHATMESSAGE_URL(CHATFLOW_ID, session_id), headers=HEADERS)

        if response.status_code == 200:
            logging.info(f"Chat history deleted successfully for session ID: {session_id}")
            return True
        else:
            logging.error(f"Failed to delete chat history. Status code: {response.status_code}, Response: {response.text}")
            return False
    except requests.RequestException as e:
        logging.error(f"Error while deleting chat history: {str(e)}")
        return False
    