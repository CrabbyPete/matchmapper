# Python imports
import requests
import json

# Import Flask
from flask                  import Flask, render_template, request, jsonify, session

# Local Locals
from config                 import SECRET_KEY

# Blueprint apps
from user                   import init_user, current_user
from forms                  import SignInForm
from event                  import event
from models.event           import Event

application = Flask(__name__, static_url_path='/static')
application.secret_key = SECRET_KEY

# Initialize the user so you can add it to the blueprint
init_user( application )
application.register_blueprint( event )

#google_map = googlemaps.Client(key='AIzaSyBD1TfgE6RnmaG6waS4_IzXbB9VmY08rqM')

@application.route('/', methods=['GET', 'POST'])
def index():
    """ Landing page 
    """
    here = {}
    sport_filter = []
    
    if request.args:
        try:
            here = {'longitude':float(request.args['lng']),'latitude':float(request.args['lat'])}
        except:
            pass
        
    ip = request.remote_addr
        
    if current_user.is_authenticated:
        if not here:
            here = {'longitude':current_user.location[1],'latitude':current_user.location[0]}
        sport_filter = current_user.sports
    
    else:
        if not here:
            ip = request.remote_addr
            url = 'http://freegeoip.net/json/{}'.format(ip)
            reply = requests.get(url)
            if reply.ok:
                data = json.loads( reply.text)
                here = {'longitude':data['longitude'],'latitude':data['latitude']}
            else:
                here ={}
        if 'sports' in session:
            sport_filter = session['sports']
        else:
            sport_filter = session['sports'] = []
        
    form = SignInForm(request.form)
    context = { 'form':form,'center':here, 'matches':[] }
    events, sports = Event.near( here, sport_filter )

    try:
        for event in events:
            point = {'longitude':str(event.location[0]),
                     'latitude' :str(event.location[1]),
                     'title':event.name,  
                     'detail':event.id,
                     'sport':event.sport.lower(),
                     'when':event.when               
                    }
            context['matches'].append( point )
        
        context['sports'] = sports
              
    except Exception as e:
        pass
            
    return render_template( 'map.html', **context )


@application.route('/ajax')
def ajax():
    event_id = request.args['id']
    record = Event.objects.get(id = event_id)
    reply = dict( name         = record.name,
                  sport        = record.sport,
                  level        = record.level,
                  where        = record.where,
                  when         = record.when,
                  good_til     = record.good_til,
                  will_host    = record.will_host,
                  will_travel  = record.will_travel,
                  fees         = record.fees
                )
    data = jsonify(reply)
    return data

@application.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@application.errorhandler(500)
def internal_error(error):
    return "500 error:{}".format( str(error) )


if __name__ == '__main__':
    application.run(debug = False,  host = '0.0.0.0' )
