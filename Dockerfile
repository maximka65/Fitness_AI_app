FROM python:3.9

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

COPY . .

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

