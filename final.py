import requests
import pandas as pd
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import json
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe
import folium

## for this project i am going to find random 20 restaurant in Soho borough in New York City.
## get the latitide and longitude of Soho, NY
address = 'Soho, NY'
geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude

## use the frousquare credential for the venue information to be fetched from foursquare API
CLIENT_ID = '4FG3Q3JIXDPNDTRRAG00HN1R4KIOKTAZI3W30XB2YVVXRXCW' # your Foursquare ID
CLIENT_SECRET = 'JKSBZKIPB4GCLGQFWITVLYWIJP23ISTOQPGLY1JSMOWIUMEO' # your Foursquare Secret
VERSION = '20180605' # Foursquare API version

## create foursquare API call URL for venue seacrh for Soho, NY. The search uses below paramteres
## limit the search result to 20, and search radius is 2000 meters from the location provided and 
## seaech is for restaurants in the area.
LIMIT = 20
radius = 2000
query = 'restaurant'
url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}&query={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    latitude, 
    longitude, 
    radius, 
    LIMIT,
    query)

results = requests.get(url).json()

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

venues = results['response']['groups'][0]['items'] ## get all the venues from the json.
nearby_venues = json_normalize(venues) # flatten JSON
# filter columns
filtered_columns = ['venue.id','venue.name', 'venue.categories', 'venue.location.lat', 'venue.location.lng']
nearby_venues =nearby_venues.loc[:, filtered_columns] ## get only the above required columns
# filter the category for each row
nearby_venues['venue.categories'] = nearby_venues.apply(get_category_type, axis=1)
nearby_venues.columns = ['Id','Name', 'Category', 'Latitude', 'Longitude'] ## rename the columns

## Since I am facing 'Quota exceeded' error with foursquare API call to get venue details, I am creating a dataframe with 
## made up data of price, likes and ratings  
d = {'Id': ['45697387f964a520e53d1fe3', '431e2d80f964a52079271fe3', '59e0ee84f0ca95526b7fce9f',
                                '55ea9f4d498ed46db0383483', '3fd66200f964a52070e91ee3', '40c10d00f964a520dd001fe3',
                                '4cc6222106c25481d7a4a047','46ff98a7f964a520234b1fe3', '5484890c498e985cf4e3c076',
                                '4f3046da7beb0cfa14dcac59','4c7d4f1b8da18cfa1afc9ece', '4f0f47650cd695a0e54cb438',
                                '3fd66200f964a520e6e51ee3','3fd66200f964a52020e61ee3', '4d9f8d97a428a1cdd92acb04',
                                '56bbc58e498eed7b2c402556','4ade0324f964a520586721e3', '49e4f405f964a52078631fe3',
                                '56ccead2498e8cad8d3cedff','5431872b498eec43384fd39d'], 
                        'price': [2,2,3,2,2,4,2,2,2,3,4,4,2,2,2,2,3,4,4,2],
                        'likes': [200,50,150,200,150,90,100,50,68,100,80,90,110,150,300,250,110,90,100,150],
                        'ratings': [4.3,4,4.5,4.5,3.5,5,4,4,3.5,4,4.5,4.5,3.5,4,4,4.5,4,4.5,4,3.5]}
final_pd = pd.DataFrame(data = d)

## below line is to merge the original venue response from Foursqaure API and dataset which contains ratings/price/likes
## information for each of the venues. This is join between 2 dataset based on Id of the venue returned by Foursquare API
final_pd = pd.merge(nearby_venues, final_pd, on = 'Id')

## below step is to create a rating column in final dataset. This rating is decided by giving different weightage to 
## acutal rating returned from Foursquare API, number of likes for the venue and average price factor for the venues
## Rating for venue has 50% weightage, Average price has a weightage of 40% and number of likes has 10% weightage.
## likes have less weightage because there are chances that many peple might have visited but not registered likes for
## a specific venue and price factor is having higher weightage as 2 venues with same rating will be differentiated by
## which is less costly. Average price has a rating from 1 to 4 (1 means less pricey and 4 being highest pricey). 
## price has been treated as a negative factor and is substracted from overall score.
final_pd['final_rating'] = final_pd.ratings * 0.5 + (final_pd.likes/50) * 0.1 - final_pd.price * 0.4
final_pd.sort_values(by='final_rating',inplace = True)
## create a map of Manhattan with all the boroughs of Manhattan plotted on it
map_soho = folium.Map(location=[latitude, longitude], zoom_start=16)

i = 21
## add markers to each venue in Soho area along with label showing name of venue, rating from Frousquare and
## comparative rating of the venue compared to the venues around it.
for lat, lng, name, rating in zip(final_pd['Latitude'], final_pd['Longitude'], final_pd['Name'], 
                                            final_pd['ratings']):
    i = i - 1
    label = 'Name: {}, rating: {}, comparative rating: {}'.format(name, rating, i)
    label = folium.Popup(label, parse_html=True)
    if(i <= 10):
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='black',
            fill=True,
            fill_color='green',
            fill_opacity=0.9).add_to(map_soho)
    else:
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='black',
            fill=True,
            fill_color='red',
            fill_opacity=0.9).add_to(map_soho)
    
map_soho.save('soho.htm') ## save the map with each of the venues in Soho
