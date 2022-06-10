FROM --platform=linux/amd64 python:3.10

WORKDIR /app
COPY ./app .
COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --reload app:app
