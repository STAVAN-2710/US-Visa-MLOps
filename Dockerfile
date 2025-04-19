# FROM python:3.8-slim

# WORKDIR /app

# # Copy only dependency files first to leverage Docker caching
# COPY pyproject.toml poetry.lock ./

# # Install Poetry and dependencies
# RUN pip install poetry && \
#     poetry config virtualenvs.create false && \
#     poetry install --no-dev --no-interaction --no-ansi

# # Copy application code
# COPY . .

# # Set Python path for proper module imports
# ENV PYTHONPATH=/app

# # Command to run the application
# CMD ["python", "app.py"]

FROM python:3.8.5-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]