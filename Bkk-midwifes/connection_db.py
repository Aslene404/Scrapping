import pymongo


def connection_mongo():
    """connect to BKK mongoDB on local"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["BKK"]
    return db


def insert_new_midwife(file_data):
    """insert extracted midwife info to mongoDB"""
    db = connection_mongo()
    result = db.midwifes.insert_one(file_data)
    return result
