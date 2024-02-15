FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/scheduler src/scheduler
COPY src/config.py src/config.py

CMD [ "arq", "src.scheduler.main.WorkerSettings" ]