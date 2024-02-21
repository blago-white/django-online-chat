FROM python:3.11.3-alpine

WORKDIR /root/chat/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /root/chat/django_chat/

ENTRYPOINT ./start.sh
