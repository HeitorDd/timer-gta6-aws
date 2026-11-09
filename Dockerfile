FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn boto3 psycopg2-binary redis
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
