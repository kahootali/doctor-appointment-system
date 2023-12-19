FROM python:3.10.13-alpine

WORKDIR /app

EXPOSE 8080

RUN pip install flask

RUN pip install flask_pymongo

COPY . .

CMD [ "python", "./app.py" ]