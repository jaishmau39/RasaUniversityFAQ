FROM python:3.7.6-stretch AS BASE

# Extend the official Rasa SDK image
FROM rasa/rasa:3.2.6

# Use subdirectory as working directory
WORKDIR /app
COPY . /app
COPY . /data /app/data

RUN rasa train

VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug"]