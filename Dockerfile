FROM python:3.12.9

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
