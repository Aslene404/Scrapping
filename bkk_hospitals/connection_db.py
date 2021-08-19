import json

import pymongo


def connection_mongo():
    """connect to care center mongoDB on local"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["BKK"]
    return db


def insert_new_hospital(file_data):
    """insert extracted care center info to mongoDB"""
    db = connection_mongo()
    result = db.hospitals.insert_one(file_data)
    return result


def get_clinic_by_street_nb_house(street, house_number):
    db = connection_mongo()
    result = db.clinics.find_one({'$and': [{"street": street,
                                            "city": house_number}]})
    return result
