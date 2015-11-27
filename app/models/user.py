import app
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient(app.config.MONGODB_URI)
mdb = client.devil

class User():
    @staticmethod
    def create(id, **kwargs):
        data = kwargs
        data['_id'] = id
        result = mdb.users.insert_one(data)
        return result.inserted_id

    @staticmethod
    def create_resource_entry(id, media_type, genre):
        # Update the user
        d = '%s.%s' % (media_type, genre)
        result = mdb.users.find_one_and_update({'_id':id, d:{'$exists': False}}, {'$set':{d:0}}, return_document=ReturnDocument.AFTER)
        return result

    @staticmethod
    def update(id, media_type, genre_type, count):
        d = {
            media_type : {
                genre_type: count
            }
        }
        result = mdb.users.update_one({'_id': id}, {'$set': d})
        return result.modified_count

    @staticmethod
    def get_next_seq(id, media_type, genre):
        d = '%s.%s' % (media_type, genre)
        result = mdb.users.find_one_and_update({'_id': id}, {'$inc': {d:1}}, return_document=ReturnDocument.AFTER)
        return result[media_type][genre]
