from pymongo     import ReadPreference

from mongoengine import connect
from config      import MONGODB as MDB


host ='mongodb://{}:{}@{}:{}/{}'.format( MDB['user'], 
                                         MDB['password'], 
                                         MDB['host'], 
                                         MDB['port'],
                                         MDB['db']        )

connect('matchmap', 
         host     = MDB['host'],
         username = MDB['user'],
         password = MDB['password'],
         port     = MDB['port'],
         read_preference=ReadPreference.PRIMARY
        )
