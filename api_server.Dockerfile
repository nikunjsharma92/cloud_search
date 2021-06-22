FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x ./api_server_entrypoint.sh
ENTRYPOINT ["./api_server_entrypoint.sh"]