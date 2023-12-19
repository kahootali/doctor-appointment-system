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

if mongo.db.doctors.count_documents({}) == 0:
    sample_doctors = [
        {
            "id": "doc1",
            "name": "Dr. John Doe",
            "specialty": "Dentist"
        },
        {
            "id": "doc2",
            "name": "Dr. Jane Doe",
            "specialty": "General Physician"
        }
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
