FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app 

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt 

CMD ["python", "3a.py"]
