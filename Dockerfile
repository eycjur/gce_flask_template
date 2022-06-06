FROM amd64/python:3.7-alpine

WORKDIR /app
COPY ./app .
COPY requirements.txt .

RUN pip install -r requirements.txt

# CMD ["gunicorn", "app:app", "-b", "0.0.0.0:$PORT"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
