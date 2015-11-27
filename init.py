import app
from app.models.user import User

import pymongo

try:
    User.create(app.config.YOUR_ID)
except pymongo.errors.DuplicateKeyError:
    print 'User %s already exists' % app.config.YOUR_ID
