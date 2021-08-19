import pymongo


def connection_mongo():
    """connect to care center mongoDB on local"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["BKK"]
    return db


def insert_new_doctor(file_data):
    """insert extracted care center info to mongoDB"""
    db = connection_mongo()
    result = db.doctors.insert_one(file_data)
    return result
