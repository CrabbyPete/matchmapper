import logging

from datetime       import datetime 
from flask          import Blueprint, render_template, request, redirect


from models.event   import Event 
from forms          import EventForm
from user           import current_user
from geo            import geocode

event = Blueprint( 'event', __name__  )

@event.route('/event', methods=['GET', 'POST'])
def add():
    """ Add a new event
    """
    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():
    
        data = dict( name    = form.name.data,
                     sport   = form.sport.data,
                     level   = form.level.data,
                     where   = form.where.data,
                     when    = form.when.data,
                     contact = current_user.id
                   )
    
        e = Event.objects( **data ).modify( upsert = True, new = True, set__modified = datetime.now() )
        try:
            e.good_til     = form.good_til.data
        except:
            e.good_til = "forever"
    
        e.will_host    = form.will_host.data
        e.will_travel  = form.will_travel.data
        e.fees         = form.fees.data
        e.restrictions = form.restrictions.data
        e.comments     = form.comments.data
        e.text         = form.text.data
    
        location       = geocode( data['where'] )
        if location:
            e.location     = [location['lng'],location['lat']]
        else:
            e.location = current_user.location
    
        try:
            e.save()
        except Exception as err:
            logging.error("Exception {} trying to save event {}".format(str(err), e))
    
    
    context = {'form':form}
    content = render_template( 'add-event.html', **context )
    return content


def events_near(location, max_distance):
    """ Find events near a location
    @param location: dict of latitude and longitude
    @param max_distance: int of max miles
    """
    query = Event.near(location, max_distance)
    return query


@event.route('/search', methods=['POST'])
def search():
    search = request.form['search_text']
    place = geocode( search )
    return redirect('/?lng={}&lat={}'.format(place[u'lng'], place[u'lat']))
