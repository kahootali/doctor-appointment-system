from flask import Flask, jsonify
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://mongo-service:27017/doctors"

mongo = PyMongo(app)

if mongo.db.doctors.count_documents({}) == 0:
    sample_doctors = [
       { 'id': "1",'firstName': "Muhammad Ali", 'lastName': "Kahoot", 'speciality':"DevOps"  },
  { 'id': "2",'firstName': "Good", 'lastName': "Doctor",'speciality':"Test"  }
    ]

    # Insert sample data
    mongo.db.doctors.insert_many(sample_doctors)

@app.route('/hello')
def hello():
    greeting = "Hello world!"
    return greeting

@app.route('/doctors', methods=["GET"])
def getDoctors():
    doctors = list(mongo.db.doctors.find())
    # Convert ObjectId to string in each doctor
    for doctor in doctors:
        doctor['_id'] = str(doctor['_id'])
    return jsonify(doctors)

@app.route('/doctor/<id>', methods=["GET"])
def getDoctor(id):
    doctor = mongo.db.doctors.find_one({"id": id})
    return jsonify(doctor)



@app.route('/health')
def health():
    return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
