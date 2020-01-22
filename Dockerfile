FROM python:3.6-alpine

COPY . /app

WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install psycopg2

RUN pip install --upgrade pip

RUN pip install flask

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", ":8080", "app:app"]
