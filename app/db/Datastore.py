from db import db
from pydoc import locate

from .. import config


class Datastore(db):

    _instance = None

    def __new__(classref, *args, **kwargs):
        """
        Uncomment the code below to instantiate a particular DB class.

        For example. In case of mongodb.
            1. Create a file mongo.py in app/db
            2. In config.py set value of `db` variable to `mongo`
            3. mongo class should extend from class `db`
        """

        """
        if not classref._instance:
            classref._instance = super(Datastore, classref).\
                    __new__(classref, *args, **kwargs)

            classref._instance.db = locate('app.db.' + config.db + '.' + config.db)()
        return classref._instance
        """
        pass
