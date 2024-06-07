FROM python:3.10.13-slim
LABEL authors="Bhuvaneshwaran"
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app