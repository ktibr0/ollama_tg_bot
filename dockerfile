FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY bot.py bot.py

CMD ["python", "bot.py"]
