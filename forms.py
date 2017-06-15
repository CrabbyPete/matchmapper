

from models.user            import User
from models.event           import Event

from wtforms                import ( validators,
                                     Form, 
                                     StringField, 
                                     PasswordField, 
                                     BooleanField,
                                     RadioField, 
                                     DateField,
                                     SubmitField,
                                    )
from wtforms.fields.html5   import TelField
from wtforms_components     import TimeField

class ValidationError( Exception ):
    pass





class SignInForm(Form):
    username = StringField( "Enter Email",
        [ validators.Email(message= u'That\'s not a valid email address.'),
          validators.Length( min = 6, max = 45)
        ]
    )
    password = PasswordField("Enter password")


class SignUpForm(Form):
    first_name  = StringField("First Name")
    last_name   = StringField("Last Name")
    
    username = StringField("Email Address", [ validators.Email(message= u'That\'s not a valid email address.'),
                                            validators.Length( min = 6, max = 45)
                                          ]
    )
    password   = PasswordField("Password")
    phone      = TelField()
    address    = StringField("Address")
    preference = RadioField('Check on best contact', choices=[('phone', 'Phone'),('email', 'Email')], default='phone')
    submit     = SubmitField("Sign Up")


class Phone( validators.Regexp ):
    def __init__(self):
        super(Phone, self).__init__( r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?', 
                                     message = "That\'s not a valid phone number")
 
class ForgotForm( Form ):
    email    = StringField( u"Email" )
    phone    = TelField()
    submit   = SubmitField("")

class EventForm( Form ):
    """ Define the user form for an event
    """
    name         = StringField(label = "Describe the event")
    sport        = StringField(label = "What sport is this?")
    level        = StringField()
    where        = StringField()
    location     = StringField()
    day          = DateField( label = "What date are you looking for?")
    time         = TimeField( label = "What time do you want to start?")
    will_host    = RadioField(label = "Will you host the match?", choices=[ (1,"Yes"),(0,"No") ], coerce = int )
    will_travel  = RadioField(choices=[ (1,"Yes"),(0,"No") ], coerce = int)
    fees         = StringField()
    restrictions = StringField()
    comments     = StringField()
    text         = RadioField(choices=[ (1,"Yes"),(0,"No") ], coerce = int)
    call         = RadioField(choices=[ (1,"Yes"),(0,"No") ], coerce = int)
    email        = RadioField(choices=[ (1,"Yes"),(0,"No") ], coerce = int)


pass
