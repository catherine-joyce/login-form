FROM python:3.9.6-slim-buster

ENV FLASK_APP=login_form

WORKDIR /app
COPY . .

# Create a non-root user
RUN useradd -m appuser

# Change ownership of the files to the non-root user
RUN chown -R appuser:appuser /app

# Give execute permission to scripts
RUN chmod +x scripts/*

# Change to the non-root user
USER appuser

RUN python3 -m venv venv

# Activate venv
ENV PATH="venv/bin:$PATH"

# Install dependencies
RUN pip3 install -e .

EXPOSE 5000

CMD ["./scripts/entrypoint.sh"]

