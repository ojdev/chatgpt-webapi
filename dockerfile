FROM python:latest

ENV access_token=
ENV CHATGPT_BASE_URL=

RUN pip install --upgrade pip && pip install flask gevent 

WORKDIR /app

COPY . .

ENTRYPOINT ["bash","entrypoint.sh","$access_token"]
