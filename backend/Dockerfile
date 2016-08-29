FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y wkhtmltopdf
RUN apt-get install -y xvfb
RUN pip3 install --upgrade pip
RUN pip3 install wheel

ADD ./utils/xvfb-wkhtmltopdf /usr/bin/

RUN mkdir -p /app/static /tmp/logs/app

VOLUME /app
VOLUME /static

WORKDIR /app
EXPOSE 8000
