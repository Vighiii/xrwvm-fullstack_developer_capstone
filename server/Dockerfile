FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

ENV APP=/app

# Change the working directory
WORKDIR $APP

# Install dependencies
COPY requirements.txt $APP/
RUN pip3 install -r requirements.txt

# Copy application code
COPY . $APP

# Expose port 8000 for the app
EXPOSE 8000

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint to run the script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Default command to start Gunicorn with 3 workers
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
