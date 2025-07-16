FROM python:3.9-slim-buster

WORKDIR /
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY code.py .
# CMD ["python","code.py"]
