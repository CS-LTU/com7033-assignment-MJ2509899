from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = None

def init_patient_db(app):
    global mongo
    app.config["MONGO_URI"] = "mongodb://localhost:27017/patient_db"
    mongo = PyMongo(app)

def add_patient(name, age, disease):
    mongo.db.patients.insert_one({"name": name, "age": age, "disease": disease})

def get_all_patients():
    return list(mongo.db.patients.find())

def get_patient(patient_id):
    return mongo.db.patients.find_one({"_id": ObjectId(patient_id)})

def update_patient(patient_id, name, age, disease):
    mongo.db.patients.update_one({"_id": ObjectId(patient_id)},
                                 {"$set": {"name": name, "age": age, "disease": disease}})

def delete_patient(patient_id):
    mongo.db.patients.delete_one({"_id": ObjectId(patient_id)})
