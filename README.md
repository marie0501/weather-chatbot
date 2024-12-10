# Weather Chatbot

This project is a weather chatbot that allows users to ask weather-related questions. The chatbot leverages the **Flowise API** for building the language model, the **OpenWeatherMap API** for retrieving weather information, and the **OpenAI API** as the core language model. The user interface is built using **Streamlit**.


## Requirements

To run the chatbot, you need to have **OpenAI API Key** and **OpenWeatherMap API Key**.

1. **OpenAI API Key**: You can get your API key from OpenAI.
2. **OpenWeatherMap API Key**: You can get your API key from OpenWeatherMap.

## Setup

Follow the steps below to set up and run the project locally or using Docker.

### 1. Clone the repository

Clone this repository to your local machine:

```bash
git clone https://github.com/marie0501/weather-chatbot.git
cd weather-chatbot
```

### 2. Create a `.env` file

In the root of the project, create a `.env` file to store your API keys. The `.env` file should contain the following keys:

```env
OPENAI_API_KEY=your_openai_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

Make sure to replace `your_openai_api_key` and `your_openweathermap_api_key` with your actual API keys.

### 3. Install Dependencies

You can either install the dependencies manually or use Docker.

#### Manually (without Docker):

1. Ensure you have **Poetry** installed on your system. If not, you can install it following the [official Poetry installation guide](https://python-poetry.org/docs/#installation).

2. Install the required dependencies using Poetry:

    ```bash
    poetry install
    ```

3. Activate the virtual environment created by Poetry (optional):

    ```bash
    poetry shell
    ```

4. Run the application:

    ```bash
    poetry run streamlit run app.py
    ```


#### Using Docker:

Alternatively, you can use Docker to run the application.

1. Ensure you have [Docker](https://www.docker.com/products/docker-desktop) installed.

2. Use Docker Compose to build and start the application:

    ```bash
    docker-compose up --build
    ```

This will automatically set up the environment and run the application.

### 4. Running the Application

If you are running the application manually (without Docker):

1. Make sure your `.env` file is in the root directory.
2. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

If you are using Docker, the application will automatically start once the container is built.

### 5. Access the Application

Once the application is running, you can access it in your browser at `http://localhost:8501` (or another port if specified in the Streamlit config).

