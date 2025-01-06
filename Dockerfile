FROM python:3.11-alpine

COPY * .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5400

ENTRYPOINT ["python", "bot.py"]