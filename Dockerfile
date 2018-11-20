# Base image
FROM python:3.6
# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN ls
RUN pip install -r ./requirements.txt