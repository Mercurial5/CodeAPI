FROM python:3.11
RUN mkdir /app
WORKDIR /app

ADD . /app/

RUN apt-get update -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz
RUN tar xzvf docker-17.04.0-ce.tgz
RUN mv docker/docker /usr/local/bin
RUN rm -r docker docker-17.04.0-ce.tgz

