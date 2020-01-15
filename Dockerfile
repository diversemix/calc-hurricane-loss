FROM python:3.7

WORKDIR /app
RUN apt-get update && apt-get -y install build-essential python3-venv python3-pip
CMD [ "make" ]
