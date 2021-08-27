import pymongo


def connection_mongo():
    """connect to mongoDB on local"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Xing"]
    return db


def connection_mongo_to_companies():
    """connect to companies mongoDB on local"""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["companies_test"]
    return mycol


def insert_new_company(file_data):
    """insert extracted company info to mongoDB"""
    db = connection_mongo()
    result = db.Companies.insert_one(file_data)
    return result
