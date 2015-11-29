import app
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

from app.db import db
from app.models.user import User, LUser
from app.exceptions import *

client = MongoClient(app.config.MONGODB_URI, connect=False)
mdb = client.devil

class Resources():
    @staticmethod
    def update(id, media_type, genre, list_items):
        total_count = mdb[media_type].find({'genre': genre}).count()
        for item in list_items:
            item['genre'] = genre
            item['seq'] = total_count + 1
            total_count = total_count + 1
        result = mdb[media_type].insert_many(list_items)
        User.create_resource_entry(id, media_type, genre)
        return result.inserted_ids

    @staticmethod
    def fetch(api_key, media_type, genre):
        d = '%s.%s' % (media_type, genre)
        user = LUser.query.filter_by(api_key=api_key).first()
        if user is None:
            raise AuthorizationException('user is not authorized to do this operation')

        document_seq = User.get_next_seq(user.id, media_type, genre)
        result = mdb[media_type].find_one({'genre': genre, 'seq': document_seq})
        result['_id'] = str(result['_id'])
        return result
