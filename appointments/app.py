from flask import Flask, jsonify
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

secrets_file_path = os.path.join(os.path.dirname(__file__), 'secrets.txt')
with open(secrets_file_path) as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.strip().split('=')
        os.environ[key] = value

# Print loaded environment variables
print(os.environ)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


mongo = PyMongo(app)

@app.route('/hello')
def hello():
  greeting = "Hello world!"
  return greeting


if mongo.db.appointments.count_documents({}) == 0:
    sample_appointments = [
        {
            "id": "app1",
            "doctor_id": "doc1",
            "patient_id": "pat1",
            "date": "2020-01-01",
            "time": "10:00"
        },
        {
            "id": "app2",
            "doctor_id": "doc1",
            "patient_id": "pat2",
            "date": "2020-01-01",
            "time": "11:00"
        },
        {
            "id": "app3",
            "doctor_id": "doc2",
            "patient_id": "pat3",
            "date": "2020-01-01",
            "time": "12:00"
        }
    ]

    # Insert sample data
    mongo.db.appointments.insert_many(sample_appointments)

@app.route('/appointments', methods=["GET"])
def getAppointments():
    appointments = list(mongo.db.appointments.find())

    # Convert ObjectId to string in each appointment
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])

    return jsonify(appointments)


@app.route('/appointments/', methods=["POST"])
def addAppointment():
  appointment = {
    "id": request.json['id'],
    "doctor_id": request.json['doctor_id'],
    "patient_id": request.json['patient_id'],
    "date": request.json['date'],
    "time": request.json['time']
  }
  mongo.db.appointments.insert(appointment)
  return jsonify(appointment)



@app.route('/appointment/<id>', methods=["GET"])
def getAppointment(id):
    appointment = mongo.db.appointments.find_one({"id": id})
    return jsonify(appointment)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070)