# Python imports
import requests
import json

# Import Flask
from flask                  import Flask, render_template, request

# Local Locals
from config                 import SECRET_KEY

# Blueprint apps
from user                   import init_user, current_user
from event                  import event
from models.event           import Event

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize the user so you can add it to the blueprint
init_user( app )
app.register_blueprint( event )


#google_map = googlemaps.Client(key='AIzaSyBD1TfgE6RnmaG6waS4_IzXbB9VmY08rqM')


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Landing page 
    """
    ip = request.remote_addr
    if current_user.is_authenticated:
        here = {'longitude':current_user.location[0],'latitude':current_user.location[1]}
    else:
        ip = request.remote_addr
        url = 'http://freegeoip.net/json/{}'.format(ip)
        reply = requests.get(url)
        if reply.ok:
            data = json.loads( reply.text)
            here = {'longitude':data['longitude'],'latitude':data['latitude']}
        else:
            here ={}
        
        
        
    events = Event.near( here )
    context = {'matches':[]}
    for event in events:
        point = {'longitude':str(event.location[0]),
                 'latitude' :str(event.location[1]),
                 'title':event.name                    
                 }
            
        context['matches'].append( point )
            

        
    return render_template( 'map.html', **context )

@app.route('/ajax')
def ajax():
    username = request.form['username']
    return jsonify(username=username)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.errorhandler(500)
def internal_error(error):
    return "500 error:{}".format( str(error) )


if __name__ == '__main__':
    app.run(debug = False,  host = '0.0.0.0' )
