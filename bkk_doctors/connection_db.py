import pymongo


def connection_mongo():
    """connect to BKK mongoDB on local"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["BKK"]
    return db


def insert_new_doctor(file_data):
    """insert extracted doctor info to mongoDB"""
    db = connection_mongo()
    result = db.doctors.insert_one(file_data)
    return result
def get_doctor_url():
    """returns the doctor's url source """

    db = connection_mongo()
    result = db.doctors.find()

    return result
def get_doctor_info(url):
    db = connection_mongo()
    result = db.doctors.find_one({"source_url": url})

    return result





