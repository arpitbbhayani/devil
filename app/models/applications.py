import app, bson
from pymongo import MongoClient

from app.db import db
from app.exceptions import *

client = MongoClient(app.config.MONGODB_URI)
mdb = client.devil

class Applications():
    @staticmethod
    def create(user, title, description, link):
        result = mdb.applications.insert_one({
            'title': title,
            'description': description,
            'link': link,
            'user': {
                'id': user.id,
                'fname': user.fname,
                'lname': user.lname
            }
        })
        return result.inserted_id

    @staticmethod
    def update(application_id, title, description, link):
        application_id = bson.ObjectId(application_id)
        mdb.applications.update_one({'_id': application_id}, { '$set': {
            'title': title,
            'description': description,
            'link': link
        }})

    @staticmethod
    def fetch(user_id):
        if user_id is None:
            results = mdb.applications.find({})
        else:
            results = mdb.applications.find({'user.id': user_id})

        applications = []
        for result in results:
            result['id'] = str(result['_id'])
            applications.append(result)
        return applications

    @staticmethod
    def fetch_all():
        results = mdb.applications.find({})

        applications = []
        for result in results:
            result['id'] = str(result['_id'])
            applications.append(result)
        return applications

    @staticmethod
    def fetch_one(application_id):
        application_id = bson.ObjectId(application_id)
        result = mdb.applications.find_one({'_id': application_id})
        if result is None:
            return None
        result['id'] = str(result['_id'])
        return result


    @staticmethod
    def delete_one(application_id):
        application_id = bson.ObjectId(application_id)
        result = mdb.applications.delete_one({'_id': application_id})
        if result is None:
            return None
        return result
