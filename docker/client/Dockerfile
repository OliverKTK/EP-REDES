FROM python:3-alpine

RUN apk update
RUN apk add iproute2
RUN pip install termcolor

COPY gameLibrary.py /usr/src/app/gameLibrary.py
COPY serverClientGame/gameClient.py /usr/src/app/client.py

WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/src/app

CMD [ "python3", "./client.py"]
