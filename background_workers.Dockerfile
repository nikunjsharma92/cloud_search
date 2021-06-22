FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x ./background_workers_entrypoint.sh
ENTRYPOINT ["./background_workers_entrypoint.sh"]