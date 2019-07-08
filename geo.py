import urllib,time,json,requests, logging

from config import GOOGLE_API_KEY
from geopy.distance import vincenty

root_url = "https://maps.googleapis.com/maps/api/geocode/json?"
distance_url = "https://maps.googleapis.com/maps/api/distancematrix/json?" #origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&key=YOUR_API_KEY


def walk(seq, look_for):
    """
    Walk through the dictionary to find a value
    """
    if isinstance( seq, list ):
        for value in seq:
            found = walk( value, look_for )
            if found:
                return found

    elif isinstance( seq, dict ):
        for key,value in seq.items():
            if key == look_for:
                return (key,value)

            if isinstance( value, dict ) or isinstance( value, list ):
                found = walk( value, look_for )
                if found:
                    return found
    return None


#https://developers.google.com/maps/documentation/geocoding/#ReverseGeocoding
def reverse_geocode(lat,lng):
    #coords = "%f,%f" %(lat,lng)
    values = {'latlng' :"%s,%s" %(lat,lng),'sensor':'false', 'key':GOOGLE_API_KEY}
    data = urllib.parse.urlencode( values )
    url = root_url+data
    response = requests.get(url)
    geodat = json.loads(response.text)
    zipcode = address = None
    for component in geodat['results']:
        types  = component.get('types', None )
        if 'postal_code' in types:
            zipcode = component['address_components'][0]['long_name']
        if 'street_address' in types:
            address = component['formatted_address']
    return address, zipcode

# https://developers.google.com/maps/documentation/geocoding/
def geocode(addr):
    # Encode our dictionary of url parameters
    values = {'address' : addr, 'sensor':'false','key':GOOGLE_API_KEY }
    data = urllib.parse.urlencode( values )
    # Set up our request
    url = root_url+data
    response = requests.get(url)
    # Get JSON data
    if response.ok:
        geodat = json.loads(response.text)
        if 'error_message' in geodat:
            logging.error(geodat['error_message'])
        else:
            location = walk( geodat, 'location')
            if location:
                return location[1]

    return None


def distance( origin, dest ):
    values = "origins={},{}%20destinations={},{}".format(origin['lat'],origin['lng'], dest['lat'],dest['lng'])
    #data = urllib.urlencode(values)
    url = distance_url+values
    response = requests.get( url )
    if response.ok:
        geodat = json.loads(response.text)
        return geodat
    return None


if __name__ == '__main__':
    reply = geocode('07481')
    me = geocode( '280 Monroe Ave, Wyckoff NJ 07481')
    reply = reverse_geocode(reply['lat'],reply['lng'] )
    allendale = geocode('Crestwood Lake, Allendale, NJ 07401')
    #reply = distance( me, allendale )
    distance = vincenty( ( float(me['lat']),float(me['lng']) ),( float(allendale['lat']),float(allendale['lng']) ) )
    print ( distance.miles )
    
    #reply = distance( reverse_geocode(me['lat'],me['lng']), reverse_geocode(allendale['lat'],allendale['lng']) )
    pass