import arrow
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
                     contact = current_user.id
                   )
        
        day = str(form.day.data) + " " + str(form.time.data)
       
        e = Event.objects( **data ).modify( upsert = True, new = True, set__modified = datetime.now() )
    
        e.when         = arrow.get(day, 'YYYY-MM-DD HH:mm:ss').datetime
        
        e.fees         = form.fees.data
        e.restrictions = form.restrictions.data
        e.comments     = form.comments.data
        
        e.will_host    = True if form.will_host.data else False
        e.will_travel  = True if form.will_travel.data else False
        e.text         = True if form.text.data else False
        e.email        = True if form.email.data else False
        e.call         = True if form.call.data else False
    
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
    content = render_template( 'event.html', **context )
    return content


@event.route('/show', methods=['GET'])
def show():
    """ Show a single event 
    """
    event_id = request.args['id']
    record = Event.objects.get(id = event_id)
    context = { 'event':dict( name         = record.name,
                              sport        = record.sport,
                              level        = record.level,
                              where        = record.where,
                              when         = record.when,
                              will_host    = record.will_host,
                              will_travel  = record.will_travel,
                              fees         = record.fees
                            )
              }
    content = render_template( 'show-event.html', **context )
    return content


@event.route('/search', methods=['POST'])
def search():
    search = request.form['search_text']
    place = geocode( search )
    return redirect('/?lng={}&lat={}'.format(place[u'lng'], place[u'lat']))
