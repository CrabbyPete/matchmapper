from flask          import Blueprint, request, render_template, redirect

from models.event   import Event 
from forms          import EventForm

from geo            import geocode

event = Blueprint( 'event', __name__  )

@event.route('/event', methods=['GET', 'POST'])
def add():
    """ Add a new event
    """
    form = EventForm(request.form)
    if not request.method == 'POST' or not form.validate():
        context = { 'form':form }
        return render_template( 'event.html', **context )

    name    = form.name.data
    sport   = form.sport.data
    level   = form.level.data
    where   = form.where.data
    when    = form.when.data
    contact = request.user

    e = Event.objects( name = name,  
                       sport = sport,
                       level = level, 
                       when = when, 
                       where = where, 
                       contact = contact
                      ).update(upsert=True)

    e.location     = geocode( where )
    e.good_til     = form.good_til.data
    e.will_host    = form.will_host.data
    e.will_travel  = form.will_travel.data
    e.fees         = form.fees.data
    e.restrictions = form.restrictions.data
    e.comments     = form.comments.data
    e.text         = form.text.data
    e.save()
    
    return redirect( '/' )

