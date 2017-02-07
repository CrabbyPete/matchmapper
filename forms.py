
import re

from models.user                    import User
from models.event                   import Event
from wtforms                        import ( Form, 
                                             TextField, 
                                             PasswordField, 
                                             BooleanField,
                                             RadioField, 
                                             SubmitField    
                                           )
from flask.ext.wtf.html5            import  TelField

from wtforms                        import validators
from flask.ext.mongoengine.wtf.orm  import model_form

class ValidationError( Exception ):
    pass

class SignInForm(Form):
    username = TextField( "Enter Email",
        [ validators.Email(message= u'That\'s not a valid email address.'),
          validators.Length( min = 6, max = 45)
        ]
    )
    password = PasswordField("Enter password")


class SignUpForm(Form):
    first_name  = TextField("First Name")
    last_name   = TextField("Last Name")
    
    username = TextField("Email Address", [ validators.Email(message= u'That\'s not a valid email address.'),
                                            validators.Length( min = 6, max = 45)
                                          ]
    )
    password   = PasswordField("Password",[ validators.Required() ])
    phone      = TextField("Cell Phone Number", [validators.Length( min = 6, max = 45)] )
    address    = TextField("Address")
    preference = RadioField('Check on best contact', choices=[('phone', 'Phone'),('email', 'Email')], default='phone')
    submit     = SubmitField("Sign Up")


class Phone( validators.Regexp ):
    def __init__(self):
        super(Phone, self).__init__( r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?', 
                                     message = "That\'s not a valid phone number")
 
class ForgotForm( Form ):
    email    = TextField( u"Email" )
    phone    = TelField(u"Phone Number",[ validators.optional(), Phone() ] )
    submit   = SubmitField("")

EventForm = model_form(Event, exclude = ('location'))
pass
