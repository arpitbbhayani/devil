import app
import bson, datetime

from pymongo import MongoClient
from pymongo.collection import ReturnDocument

from flask.ext.login import UserMixin
from app.db import db


client = MongoClient(app.config.MONGODB_URI, connect=False)
mdb = client.devil

class LUser(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}

    id          = db.Column(db.String(24), primary_key=True)
    social_id   = db.Column(db.String(64), nullable=False, unique=True)
    fname       = db.Column(db.String(64), nullable=False)
    lname       = db.Column(db.String(64), nullable=False)
    email       = db.Column(db.String(64), nullable=True)
    role        = db.Column(db.String(64), nullable=False, default='user')
    created_at  = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())
    last_login  = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())
    api_key     = db.Column(db.String(56))


class User():
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
