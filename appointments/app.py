from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo.errors import PyMongoError

app = Flask(__name__)

# MongoDB configuration
app.config['MONGO_URI'] = "mongodb://mongo-service:27017/appointments"
mongo = PyMongo(app)

# Sample appointments data
sample_appointments = [
    {'id': "1", 'doctor': "1", 'date': "21 Nov 2023", 'rating': "Good"},
    {'id': "2", 'doctor': "1", 'date': "22 Nov 2023", 'rating': "Bad"},
    {'id': "3", 'doctor': "2", 'date': "22 Nov 2023", 'rating': "Good"},
    {'id': "4", 'doctor': "1", 'date': "22 Nov 2023", 'rating': "Bad"},
    {'id': "5", 'doctor': "2", 'date': "22 Nov 2023", 'rating': "Good"},
]

# Insert sample data
try:
    mongo.db.appointments.insert_many(sample_appointments)
except PyMongoError as e:
    print(f"Error inserting sample data: {e}")

@app.route('/hello')
def hello():
    greeting = "Hello world!"
    return greeting

@app.route('/appointments', methods=["GET"])
def getAppointments():
    try:
        appointments = list(mongo.db.appointments.find())

        # Convert ObjectId to string in each appointment
        for appointment in appointments:
            appointment['_id'] = str(appointment['_id'])

        return jsonify(appointments)

    except PyMongoError as e:
        return jsonify({'error': f"Error retrieving appointments: {e}"}), 500

@app.route('/appointments/', methods=["POST"])
def addAppointment():
    try:
        appointment = {
            "id": request.json.get('id'),
            "doctor_id": request.json.get('doctor_id'),
            "patient_id": request.json.get('patient_id'),
            "date": request.json.get('date'),
            "time": request.json.get('time')
        }

        mongo.db.appointments.insert_one(appointment)
        return jsonify(appointment)

    except PyMongoError as e:
        return jsonify({'error': f"Error adding appointment: {e}"}), 500

@app.route('/appointment/<id>', methods=["GET"])
def getAppointment(id):
    try:
        appointment = mongo.db.appointments.find_one({"id": id})
        if appointment:
            # Convert ObjectId to string
            appointment['_id'] = str(appointment['_id'])
            return jsonify(appointment)
        else:
            return jsonify({'error': 'Appointment not found'}), 404

    except PyMongoError as e:
        return jsonify({'error': f"Error retrieving appointment: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070)
