# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir -U pip poetry

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock ./

# Install Python dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code to the working directory
COPY . .

# Copy the entrypoint script and make it executable
#COPY docker-entrypoint.sh /app/docker-entrypoint.sh
#RUN chmod +x /app/docker-entrypoint.sh

# Set the entrypoint to use the custom entrypoint script
#ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Expose the port your application will run on
EXPOSE 8501

# The default command (can be overridden by Docker Compose or at runtime)
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port", "8501"]
