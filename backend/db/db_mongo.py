from pymongo import MongoClient

client = None
db = None

def connect_mongo():
    global client, db

    MONGO_URI = (
        "mongodb+srv://muzamilhabib529_db_user:mxTfQZU8gpXce3QQ@cluster1.sv5zxbm.mongodb.net/"
        "?retryWrites=true&w=majority"
    )

    try:
        client = MongoClient(MONGO_URI)
        db = client["hospital_db"]   # database name
        print("MongoDB Atlas connected")
    except Exception as e:
        print("MongoDB connection failed:", e)
        client = None

def get_patients_collection():
    if client is None:
        raise Exception("MongoDB not connected")
    return db["patients"]
