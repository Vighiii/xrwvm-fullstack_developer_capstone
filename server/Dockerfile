# Use the official Python base image
FROM python:3.12.0-slim-bookworm

# Set environment variables
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app

# Set the working directory inside the container
WORKDIR $APP

# Copy the requirements.txt file into the container
COPY requirements.txt $APP

# Install the required Python packages
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy the rest of the application files into the container
COPY . $APP

# Expose the application port (e.g., 8000)
EXPOSE 8000

# Make sure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Set the entry point for the application
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Run the application with Gunicorn server (or any command to start the app)
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
