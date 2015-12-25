import app
import random

from app.db import db
from app.exceptions import *

class Resources():
    @staticmethod
    def update(media_type, genre, list_items):
        total_count = mdb[media_type].find({'genre': genre}).count()
        inserted_items, failed_items = [], []
        for item in list_items:
            item['genre'] = genre
            item['seq'] = total_count + 1
            try:
                result = mdb[media_type].insert_one(item)
                item.pop('_id')
                inserted_items.append(item)
                total_count = total_count + 1
            except Exception as e:
                print 'failed: ', item, e.__dict__
                item.pop('_id')
                item.pop('seq')
                failed_items.append(item)
        return inserted_items, failed_items

    @staticmethod
    def fetch(api_key, media_type, genre):
        d = '%s.%s' % (media_type, genre)
        user = LUser.query.filter_by(api_key=api_key).first()
        if user is None:
            raise AuthorizationException('user is not authorized to do this operation')

        # document_seq = User.get_next_seq(user.id, media_type, genre)
        total_count = mdb[media_type].find({"genre": genre}).count()
        if total_count == 0:
            return None

        document_seq = random.randint(1, total_count)
        result = mdb[media_type].find_one({'genre': genre, 'seq': document_seq})
        result.pop('_id')
        return result
