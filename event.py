import json

from datetime       import datetime 
from flask          import Blueprint, request, render_template, redirect

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
    if not request.method == 'POST':
        context = { 'errors':form.errors }
        return json.dumps( context )
    
    data = dict( name    = form.name.data,
                 sport   = form.sport.data,
                 level   = form.level.data,
                 where   = form.where.data,
                 when    = form.when.data,
                 contact = current_user.id
                )
    e = Event.objects( **data ).modify( upsert = True, set__modified = datetime.now() )

    e.location     = geocode( data['where'] )
    e.good_til     = form.good_til.data
    e.will_host    = form.will_host.data
    e.will_travel  = form.will_travel.data
    e.fees         = form.fees.data
    e.restrictions = form.restrictions.data
    e.comments     = form.comments.data
    e.text         = form.text.data
    e.save()
    
    context = {}
    return json.dumps( context )

@event.route('/search', methods=['POST'])
def search():
    search = request.form.text.data
    return redirect('/')
