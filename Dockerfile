FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY /app .

RUN pyi-makespec main.py

CMD [ "python", "main.py" ]