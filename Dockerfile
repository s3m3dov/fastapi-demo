# Pull base image
FROM python:3.10-alpine
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /app
# Entry point
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
# Install poetry
RUN python3 -m pip install poetry
# Install dependencies
COPY pyproject.toml pyproject.toml
RUN poetry env use python3.10
RUN poetry install --no-interaction --no-ansi
# Copy project
COPY . /app
