FROM python:3.11-slim

WORKDIR /app

# Copy requirements file from the parent directory
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy booking service contents into the container at /app
COPY booking_service/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
