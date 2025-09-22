FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

WORKDIR /app

# Install the requirements
COPY server/requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy the rest of the files
COPY . /app/

EXPOSE 8000

# Create entrypoint script
RUN echo '#!/bin/bash\ncd server\npython manage.py migrate\npython manage.py collectstatic --noinput\nexec "$@"' > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--chdir", "server", "djangoproj.wsgi"]
