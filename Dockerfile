FROM python:3.10

RUN apt-get update && apt-get install libpq-dev python-dev -y

WORKDIR /whitebox

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ENV=dev uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 
