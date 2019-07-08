# Python imports
import requests
import json

# Import Flask
from flask  import Flask, render_template, request, jsonify, session

# Local Locals
from config import SECRET_KEY, GEO_API_KEY

# Blueprint apps
from user   import init_user, current_user
from forms  import SignInForm
from event  import event
from models import Event


application = Flask(__name__, static_url_path='/static')
application.secret_key = SECRET_KEY


# Initialize the user so you can add it to the blueprint
init_user(application)
application.register_blueprint(event)

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
            ip = request.remote_addr if not request.remote_addr == '127.0.0.1' else '173.70.202.157'
            url = f'http://api.ipstack.com/{ip}?access_key={GEO_API_KEY}&output=json'
            try:
                reply = requests.get(url)
            except Exception as e:
                here = {'longitude':-74.2081,'latitude':41.0112}
            else:
                if reply.ok:
                    data = json.loads( reply.text)
                    if data['longitude'] == 0 and data['latitude'] == 0:
                        data['longitude'] = -74.1645
                        data['latitude'] = 40.9987
                        here = {'longitude':data['longitude'],'latitude':data['latitude']}
                    else:
                        here ={'longitude':data['longitude'],'latitude':data['latitude'] }
                else:
                    here = {'longitude': -74.2081, 'latitude': 41.0112}
        
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
            
    return render_template( 'index.html', **context )


@application.route('/ajax')
def ajax():
    event_id = request.args['id']
    record = Event.objects.get(id = event_id)
    reply = dict( name         = record.name,
                  sport        = record.sport,
                  level        = record.level,
                  where        = record.where,
                  when         = record.when,
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
    return "500 error:{}".format( str(error))


if __name__ == '__main__':
    application.run(host = '127.0.0.1')
