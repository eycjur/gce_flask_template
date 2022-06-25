FROM --platform=linux/amd64 python:3.10

COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
