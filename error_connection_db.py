import pymongo


def connection_mongo():
    """connect to error mongoDB on local"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Error"]
    return db
def insert_new_error(file_data):
    """insert error log to mongoDB"""
    db = connection_mongo()
    result = db.logs.insert_one(file_data)
    return result
def is_exit_with_error():
    """returns if the program exited with an error last time """
    res_ex=""
    db = connection_mongo()
    result = db.logs.find({"exit_with_error": 1})
    for re in result:
        res_ex = re
    return res_ex