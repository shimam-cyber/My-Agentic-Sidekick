# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your application will listen on
EXPOSE 7860

# Set the environment variable to ensure Gradio listens on all network interfaces
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Define the command to run your application
CMD ["python", "app.py"]
