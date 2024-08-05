FROM python:alpine

WORKDIR /bolivares-dolares-bot

RUN apk update && apk upgrade 

RUN adduser -D -h /home/user -G users user && \
    chown user:users .

COPY --chown=user:users ./app ./app
COPY --chown=user:users ./requirements ./requirements
COPY --chown=user:users ./tests ./tests

RUN pip install -r ./requirements/common.txt \
    -r ./requirements/development.txt