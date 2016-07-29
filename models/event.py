
from mongoengine    import ( Document,
                             StringField, 
                             GeoPointField, 
                             DateTimeField, 
                             BooleanField, 
                             ReferenceField,
                             queryset_manager
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

    @queryset_manager
    def within(doc_cls, queryset, location_box ):
        """ Get all events with a geographic location
        """
        data = queryset.filter( user = user )
        return data
    
    def __unicode__(self):
        return self.name