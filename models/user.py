import re, hashlib

from datetime       import datetime

from mongoengine    import ( Document, 
                             ValidationError, 
                             StringField, 
                             EmailField, 
                             GeoPointField, 
                             DateTimeField, 
                             BooleanField, 
                             ReferenceField,
                             CASCADE
                            )


class PhoneField(StringField):          # Validate phone numbers

    PHONE_REGEX = re.compile(r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?')

    def validate(self, value):
        if not value == '':
            if not PhoneField.PHONE_REGEX.match(value):
                raise ValidationError('Invalid Phone number: %s' % value)


# User Profile, also used for those not signed in
class User( Document ):
    username      = StringField( required = True )
    password	  = StringField( required = True )
    first_name	  = StringField()
    last_name	  = StringField()
    phone         = PhoneField( default = None, required = False)
    address       = StringField( default = None)
    preference    = StringField()
    location	  = GeoPointField()
    joined        = DateTimeField( default = datetime.now() )

    # Login booleans
    active        = BooleanField( default = True  )
    authenticated = BooleanField( default = False )


    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str( self.pk )

    def set_password(self, raw_password):
        h = hashlib.md5()
        h.update(raw_password)
        self.password = h.hexdigest()

    def check_password(self, raw_password):
        h = hashlib.md5()
        h.update(raw_password)
        if self.password == h.hexdigest():
            return True

        return False

    meta = { 'indexes' : ['username']
           }

    def __unicode__(self):
        if self.last_name and self.first_name:
            return self.last_name + ','+self.first_name
        return self.username

    
class Subscription( Document ):
    user     = ReferenceField( 'User', reverse_delete_rule = CASCADE )
    expires  = DateTimeField( default = datetime.now() )
    active   = BooleanField(default = False)

    meta = { 'indexes' : ['user'] }
