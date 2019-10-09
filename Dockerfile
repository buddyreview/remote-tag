FROM python:3.7-alpine

RUN pip install requests

ARG APP_DIR=/root
WORKDIR ${APP_DIR}
COPY remote_tag.py ${APP_DIR}
