FROM python:3.8

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev netcat gettext -y

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY . /app/
