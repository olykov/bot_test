FROM python:3.11-alpine

COPY * .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "bot.py"]
