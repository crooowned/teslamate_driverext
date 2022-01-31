FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r src/requirements.txt

CMD [ "python3", "-u","src/run.py" ]
