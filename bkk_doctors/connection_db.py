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


def is_exit_with_error():
    """returns if the program exited with an error last time """
    db = connection_mongo()
    result = db.doctors.find({"exit_with_error": 1})
    for re in result:
        res_ex = re
    return res_ex
