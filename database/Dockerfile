# Sử dụng image Python chính thức
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY load-data.py .

CMD ["python", "load-data.py"]