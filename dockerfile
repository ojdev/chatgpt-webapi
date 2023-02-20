FROM python:latest

ENV access_token=""

RUN pip install --upgrade pip && pip install flask && pip3 install revChatGPT

WORKDIR /app

COPY . .

ENTRYPOINT ["bash","entrypoint.sh","$access_token"]
