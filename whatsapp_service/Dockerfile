FROM python:3.12.4-slim

WORKDIR /app

COPY app.py /app
COPY Dockerfile /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8502

CMD [ "python", "app.py"]