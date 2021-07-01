# syntax=docker/dockerfile:1

FROM python:3.8.11

WORKDIR /app

COPY . .
RUN pip3 install -qU -r requirements.txt

EXPOSE 5000

CMD [ "python3", "run.py" ]