FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file from parent directory
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy current directory contents into the container at /app
COPY concert_service/ .

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
