from app import app
from flask.ext.mongoengine import MongoEngine

db = MongoEngine(app)
