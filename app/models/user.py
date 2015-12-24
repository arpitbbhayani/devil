import app
import bson

from flask.ext.login import UserMixin
from app.db import db

class Profile(db.Document, UserMixin):
    social_id   = db.StringField(unique=True)
    name       = db.StringField(required=True)
    email       = db.StringField(unique=True, required=True)
    role        = db.StringField(required=True, default="user")
    created_at  = db.DateTimeField()
    last_login  = db.DateTimeField()
    api_key     = db.StringField(unique=True)

    meta = {
        'collection': 'profiles'
    }


class UserStats(db.Document, UserMixin):
    @staticmethod
    def create(id, **kwargs):
        data = kwargs
        data['_id'] = bson.ObjectId(id)
        result = mdb.users.insert_one(data)
        return result.inserted_id

    @staticmethod
    def create_resource_entry(id, media_type, genre):
        # Update the user
        d = '%s.%s' % (media_type, genre)
        result = mdb.users.find_one_and_update({'_id':bson.ObjectId(id), d:{'$exists': False}}, {'$set':{d:0}}, return_document=ReturnDocument.AFTER)
        return result

    @staticmethod
    def update(id, media_type, genre_type, count):
        d = {
            media_type : {
                genre_type: count
            }
        }
        result = mdb.users.update_one({'_id': bson.ObjectId(id)}, {'$set': d})
        return result.modified_count

    # @staticmethod
    # def get_next_seq(id, media_type, genre):
    #     d = '%s.%s' % (media_type, genre)
    #     result = mdb.users.find_one_and_update({'_id': id}, {'$inc': {d:1}}, return_document=ReturnDocument.AFTER)
    #     return result[media_type][genre]
