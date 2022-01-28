FROM python:3.9-slim
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /config
ADD /config/requirements.txt /config/
RUN pip install --upgrade pip
RUN pip install -r /config/requirements.txt
RUN apt -y update
RUN apt list --upgradable
RUN mkdir -p /speechtotext-api
COPY assets /assets
WORKDIR /speechtotext-api
