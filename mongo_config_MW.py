import pymongo


def connection_mongo():
    """connect to mongo on local"""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["MidWifes"]
    return mycol


if __name__ == "__main__":
    connection_mongo()
