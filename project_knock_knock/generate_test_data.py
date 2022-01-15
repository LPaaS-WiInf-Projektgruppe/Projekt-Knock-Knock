from Models import User, DriverOffers, ComOffers, Rating
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import distance
from extensions import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_knock_knock.db'
db = SQLAlchemy(app)

from datetime import datetime

start_location = "Kressenweg 14, Hamburg"

# geocode the location
geolocator = Nominatim(user_agent="project_knock_knock")
start_coords = geolocator.geocode(start_location)
# end_coords = geolocator.geocode(content_ende)
start_time = datetime.strptime("23.11.2022-08:00", '%d.%m.%Y-%H:%M')
end_time = datetime.strptime("23.11.2022-08:00", '%d.%m.%Y-%H:%M')

rating = Rating()

start_lat = start_coords.latitude
start_long = start_coords.longitude

print(f"start_lat{start_lat}")

end_lat = start_coords.latitude
end_long = start_coords.longitude

locations = []

for i in range(0, 5, 1):
    for j in range(0, 10, 1):
        start_lat = start_coords.latitude +  i/ 50 - .05
        start_long = start_coords.longitude +  j/ 50
        end_lat = start_coords.latitude + i/ 50 - 0.01
        end_long =  start_coords.longitude + j/ 50 -0.01

        user = User(
            username =f"Test {i * 10 + j}",
            password = f"Test {i * 10 + j}"
        )

        com_offer = ComOffers(
            start = f"Test Start {i * 10 + j} ",
            start_lat = start_lat,
            start_long = start_long,
            end_lat = end_lat,
            end_long = end_long,
            destination = f"Test Destination {i * 10 + j}" ,
            start_time = start_time,
            end_time = end_time,
            kilometerpreis = 0.99,
            creator = user,
            rating = rating
        )

        db.session.add(com_offer)
db.session.commit()
# print(f'the locations are {locations}')
