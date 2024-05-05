# Use the official Python image as the base image
FROM python:latest

# Set the working directory
WORKDIR /app

# Copy your Django application code into the container
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port your Django app will run on
EXPOSE 8090

# Define the command to start your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8090"]
