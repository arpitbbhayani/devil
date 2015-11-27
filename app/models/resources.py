import app
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

from app.models.user import User

client = MongoClient(app.config.MONGODB_URI)
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
    def fetch(id, media_type, genre):
        d = '%s.%s' % (media_type, genre)
        document_seq = User.get_next_seq(id, media_type, genre)
        result = mdb[media_type].find_one({'genre': genre, 'seq': document_seq})
        result['_id'] = str(result['_id'])
        return result
