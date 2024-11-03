# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the poetry files first for better caching
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Specify the command to run your application using Poetry
CMD ["poetry", "run", "streamlit", "run", "inventory_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
