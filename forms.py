

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
                                     TextField
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
    name         = StringField( label = "Describe the event?" )
    sport        = StringField( label = "What sport is this?" )
    level        = StringField( label = "What level is this?" )
    where        = StringField( label = "Whats the full address of the location")
    location     = StringField()
    day          = DateField( label = "What date are you looking for?" , format='%m/%d/%Y' )
    time         = TimeField( label = "What time do you want to start?" )
    will_host    = RadioField(label = "Are you willing to host the game?", choices=[ (1,"Yes"),(0,"No") ], default = 1, coerce = int )
    will_travel  = RadioField( label = "Are you willing to travel to the game?", choices=[ (1,"Yes"),(0,"No") ], default = 1, coerce = int)
    fees         = StringField( label = "Are there any associated fees such as referees or venue fees?")
    restrictions = StringField( label = "Are there any restrictions such as weights")
    comments     = TextField( label = "Any further comments?" )
    text         = RadioField( label = "Would you like opponents to text you?",  choices=[ (1,"Yes"),(0,"No") ], default = 1, coerce = int)
    call         = RadioField( label = "Would you like opponents to call you?",   choices=[ (1,"Yes"),(0,"No") ], default = 1, coerce = int)
    email        = RadioField( label = "Would you like opponents to email you",  choices=[ (1,"Yes"),(0,"No") ], default = 1, coerce = int)
    submit      = SubmitField("")


