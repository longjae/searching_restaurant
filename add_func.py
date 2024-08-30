import os
from decimal import Decimal

from dotenv import load_dotenv
from geopy.geocoders import GoogleV3

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def to_lat_lng(content):
    geolocator = GoogleV3(api_key=GOOGLE_MAPS_API_KEY)
    
    location = geolocator.geocode(content) 
    
    if location:
        return location.latitude, location.longitude
    else:
        print("위치 정보를 찾을 수 없습니다.")