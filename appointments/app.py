from flask import Flask, jsonify
from flask_pymongo import PyMongo
import os

app = Flask(__name__)


app.config['MONGO_URI'] = "mongodb://mongo-service:27017/appointments"


mongo = PyMongo(app)

@app.route('/hello')
def hello():
  greeting = "Hello world!"
  return greeting


if mongo.db.appointments.count_documents({}) == 0:
    sample_appointments = [
        { 'id': "1",'doctor': "1", 'date': "21 Nov 2023", 'rating':"Good"  },
  { 'id': "2",'doctor': "1", 'date': "22 Nov 2023", 'rating':"Bad"  },
  { 'id': "3",'doctor': "2", 'date': "22 Nov 2023", 'rating':"Good"  },
  { 'id': "4",'doctor': "1", 'date': "22 Nov 2023", 'rating':"Bad"  },
  { 'id': "5",'doctor': "2", 'date': "22 Nov 2023", 'rating':"Good"  },
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