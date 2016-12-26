import random
import json

from mailer                 import Mailer, Message

from flask                  import Blueprint, render_template, request, redirect

from flask.ext.login        import ( LoginManager, 
                                     login_required, 
                                     login_user, 
                                     logout_user, 
                                     current_user
                                    )

from models.user            import User
from forms                  import SignInForm, SignUpForm, ForgotForm

from geo                    import geocode
from config                 import EMAIL
from log                    import log


user = Blueprint( 'user', __name__  )

login_manager = LoginManager()

def init_user(app):
    login_manager.setup_app(app)
    app.register_blueprint(user)
    pass


@login_manager.user_loader
def load_user(userid):
    """ Used by login to get a user """
    try:
        user = User.objects.get( pk = userid )
    except:
        return None
    return user


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Signup a new user 
    """
    form = SignUpForm(request.form)
    if not request.method == 'POST'or not form.validate():
        context = { 'error':"Not valid",'form':form }
        return json.dumps(context)

    first_name = form.first_name.data
    last_name  = form.last_name.data
    username   = form.username.data
    password   = form.password.data
    preference = form.preference.data
    phone      = form.phone.data
    address    = form.address.data

    # Check if they they exist already
    context = {}
    try:
        user = User.objects.get( username = username )
    except User.DoesNotExist:
        user = User( username = username )
        user.first_name    = first_name
        user.last_name     = last_name
        user.address       = address
        user.phone         = phone
        user.address       = address
        user.preference    = preference
        user.set_password( password )
        try:
            local = geocode( user.address )
            user.location = [ float(local['lat']), float(local['lng']) ]
        except Exception, e:
            pass

        try:
            user.save()
        except Exception, e:
            print e
    else:
        context = { 'error':'User already exists', 'form':form }
        return json.dumps( context )

    login_user( user )
    return redirect('/')
    
@user.route('/signin', methods=['GET', 'POST'])
def signin():
    """ Login a user
    """
    form = SignInForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        if username:
            try:
                user = User.objects.get( username = username )
            except User.DoesNotExist:
                form.username.errors = ['No such user or password']
            else:
                if not user.check_password(password):
                    form.username.errors = ['No such user or password']
                else:
                    login_user(user)
                    return  render_template('close-iframe.html')
        else:
            form.username.errors = ['Enter an email address']
   
    # Not a POST or errors
    context = {'form':form}
    content = render_template( 'signin.html', **context )
    return content


@user.route('/signout')
@login_required
def signout():
    """ Logout a user
    """
    logout_user()
    return redirect('/')


def send_email( user, password ):
    """ Send new password to user
    """
    
    mail  = Mailer( host    = EMAIL['host'], 
                    port    = EMAIL['port'],
                    use_tls = EMAIL['use_tls'], 
                    usr     = EMAIL['user'], 
                    pwd     = EMAIL['password']
                  )
                   
    message = Message( From    = 'help@matchmapper.com',
                       To      = [user.email],
                       Subject = "Password Reset"
                     )
    
    body = """Your new password for {} is {}
              You can reset it to what you like on your settings page once you log in with
              this password
           """.format(__name__, password )

    message.Body = body
    try:
        mail.send(message)
    except Exception, e:
        log('Send mail error: {}'.format(str(e)))


@user.route( '/forgot', methods=['GET','POST'] )
def forgot():
    form = ForgotForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data
        try:
            user = User.objects.get( email = email )
        except User.DoesNotExist:
            form.email.errors = ['No such user']
            context = {'form':form}
            return render_template('forgot.html', **context )

        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        password = ''.join( map( lambda x: random.choice(chars), range(8) ))
        user.set_password( password )
        user.save()
        
        #send_email( user, password )
        return redirect('/signin')
    else:
        context = {'form':form}
        return render_template('forgot.html', **context )
