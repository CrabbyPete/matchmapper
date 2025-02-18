
from mongoengine    import ( Document,
                             StringField, 
                             GeoPointField, 
                             DateTimeField,
                             BooleanField, 
                             ReferenceField
                            )
                             

class Event( Document ):
    name         = StringField()
    sport        = StringField()
    level        = StringField()
    where        = StringField()
    location	 = GeoPointField()
    when         = DateTimeField()
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
    def near(cls, location, sport_filter = [], max_distance = 10 ):
        """ Get all events with a geographic location
        @param location: dict of longitude and latitude
        @param max_distance: maximum distance in miles
        """
   
        query = cls.objects(location__near=[location['longitude'],location['latitude']], location__max_distance = max_distance)
        
        sports = {}
        events = []
        try:
            for event in query:
                if not event.sport.lower() in sports:
                    sports[event.sport.lower()] = event.sport.lower() in sport_filter

                if sport_filter:
                    if event.sport.lower() in sport_filter:
                        events.append(event)
                else:
                    events.append(event)
        except RuntimeError as e:
            # Mongo engine is not 3.7 ready, so it bubbles up StopInteration. Catch it here
            # if str(e) == 'generator raised StopIteration':
            pass

        return events, sports
        

    @classmethod
    def find_or_create(cls):
        pass
        
        
        
    def __unicode__(self):
        return self.name