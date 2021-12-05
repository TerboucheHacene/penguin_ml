FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV APP_MODULE app.app:app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
COPY ./models/ /app/models