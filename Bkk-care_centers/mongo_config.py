import json

import pymongo


def connection_mongo():
    """connect to care center mongoDB on local"""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["BKK"]
    mycol = mydb["Care"]
    return mycol
def insert_mongo(res,mycol):
    """insert extracted care center info to mongoDB"""
    final_string = json.dumps(res)
    print(final_string)
    file_data = json.loads(final_string)
    print(file_data)
    xs = mycol.insert_one(file_data)
    output="Successfully inserted into mongo database with id " + str(xs.inserted_id)
    return output