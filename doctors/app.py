from flask import Flask, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import PyMongoError

app = Flask(__name__)

# MongoDB configuration
app.config['MONGO_URI'] = "mongodb://mongo-service:27017/doctors"
mongo = PyMongo(app)

# Sample doctors data
sample_doctors = [
    {'id': "1", 'firstName': "Muhammad Ali", 'lastName': "Kahoot", 'speciality': "DevOps"},
    {'id': "2", 'firstName': "Good", 'lastName': "Doctor", 'speciality': "Test"},
]

# Insert sample data
try:
    mongo.db.doctors.insert_many(sample_doctors)
except PyMongoError as e:
    print(f"Error inserting sample data: {e}")

@app.route('/hello')
def hello():
    greeting = "Hello world!"
    return greeting

@app.route('/doctors', methods=["GET"])
def getDoctors():
    try:
        doctors = list(mongo.db.doctors.find())

        # Convert ObjectId to string in each doctor
        for doctor in doctors:
            doctor['_id'] = str(doctor['_id'])

        return jsonify(doctors)

    except PyMongoError as e:
        return jsonify({'error': f"Error retrieving doctors: {e}"}), 500

@app.route('/doctor/<id>', methods=["GET"])
def getDoctor(id):
    try:
        doctor = mongo.db.doctors.find_one({"id": id})
        if doctor:
            # Convert ObjectId to string
            doctor['_id'] = str(doctor['_id'])
            return jsonify(doctor)
        else:
            return jsonify({'error': 'Doctor not found'}), 404

    except PyMongoError as e:
        return jsonify({'error': f"Error retrieving doctor: {e}"}), 500

@app.route('/health')
def health():
    return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
