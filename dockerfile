FROM python:latest

ENV access_token=

RUN pip install --upgrade pip && pip install flask gevent revChatGPT

WORKDIR /app

COPY . .

ENTRYPOINT ["bash","entrypoint.sh","$access_token"]
