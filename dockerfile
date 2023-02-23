FROM python:latest

ENV access_token=

RUN pip install --upgrade pip && pip install flask gevent 
RUN pip install "git+https://github.com/acheong08/ChatGPT"

WORKDIR /app

COPY . .

ENTRYPOINT ["bash","entrypoint.sh","$access_token"]
