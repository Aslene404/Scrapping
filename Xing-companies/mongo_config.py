import pymongo


def connection_mongo():
    """connect to mongo on local"""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["Xing"]
    return mycol
def connection_mongo_to_companies():
    """connect to mongo on local"""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["companies_test"]
    return mycol


if __name__ == "__main__":
    connection_mongo()
