
from mongoengine    import ( Document,
                             StringField, 
                             GeoPointField, 
                             DateTimeField, 
                             BooleanField, 
                             ReferenceField
                            )
                             

class Event( Document ):
    name		 = StringField()
    sport        = StringField()
    level        = StringField()
    where        = StringField()
    location	 = GeoPointField()
    when         = DateTimeField()
    good_til     = DateTimeField()
    will_host    = BooleanField()
    will_travel  = BooleanField()
    fees         = StringField()
    restrictions = StringField()
    comments     = StringField()
    text         = BooleanField()
    call         = BooleanField()
    email        = BooleanField()
    modified     = DateTimeField()
    contact      = ReferenceField('User')


    @classmethod
    def near(cls, location, max_distance = 1000 ):
        """ Get all events with a geographic location
        @param location: dict of longitude and latitude
        @param max_distance: maximum distance in miles
        """
        query = cls.objects(location__near=[location['longitude'],location['latitude']])#, location__max_distance = max_distance )
        return query

    def __unicode__(self):
        return self.name