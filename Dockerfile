
# Use the official Python 3.10 slim image based on Debian Bullseye as the base image
FROM python:3.10-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY src/requirements.txt /app/requirements.txt

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code to the working directory
COPY src/ /app/

# Expose port 8000 for the application
EXPOSE 8000

# Define the command to run the application with Uvicorn
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]