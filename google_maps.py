import json
import os

import googlemaps
from dotenv import load_dotenv

from add_func import decimal_default, to_lat_lng

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)

def search_maps(content):
    print(f"SEARCHING MAPS for {content}=======================")
    lat, lng = to_lat_lng(content)
    places_result = gmaps.places_nearby(
        # location="Wonhyo-ro 1 ga, Yongsan-gu, Seoul, Korea", 
        location=(lat, lng),
        radius=500,
        keyword="restaurant",
        language="ko"
    )
    if places_result.get("results"):
        places_data = []
        for place in places_result["results"]:
            place_data = {
                "Name": place.get("name"),
                "Address": place.get("vicinity"),
                "Rating": place.get("rating"),
                "Business_status": "영업중" if place.get("business_status") == "OPERATIONAL" else "휴무"
            }
            places_data.append(place_data)
            
    for place in places_data:
        print(place)
        

    json_data = json.dumps(places_data, indent=4, default=decimal_default, ensure_ascii=False)
    # print(json_data)

    with open("data.txt", "w") as file:
        file.write(json_data)