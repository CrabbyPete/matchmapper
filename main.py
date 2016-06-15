# Python imports

#import googlemaps

# Import Flask
from flask                  import Flask, render_template, redirect, url_for

from config                 import SECRET_KEY

# Blueprint apps
from user                   import user, init_user, current_user
from event                  import event

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize the user so you can add it to the blueprint
init_user( app )
app.register_blueprint( event )
#app.register_blueprint( user )

#google_map = googlemaps.Client(key='AIzaSyBD1TfgE6RnmaG6waS4_IzXbB9VmY08rqM')

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Landing page 
    """
    if current_user.is_authenticated:
        context = {'user': current_user,
                   'matches':[{'Raiders football':{'longitude':'-74.168981','latitude':'41.0076139'} }]
                  }

        #gmap = google_map.geocode('280 Monroe Ave, Wyckoff NJ')
    else:
        context = {}
        
    return render_template( 'map.html', **context )


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
"""
@app.errorhandler(500)
def internal_error(error):
    return "500 error:{}".format( str(error) )
"""
if __name__ == '__main__':
    app.run(debug = False,  port=8000)
