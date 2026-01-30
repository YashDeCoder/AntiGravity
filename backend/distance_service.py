import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")
NS_API_KEY = os.getenv("NS_API_KEY")

def geocode_address(address: str):
    """
    Converts an address string to coordinates using OpenRouteService.
    """
    if not ORS_API_KEY or ORS_API_KEY == "your_ors_api_key_here":
        return None

    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": ORS_API_KEY,
        "text": address,
        "boundary.country": "NL",
        "size": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['features']:
            coords = data['features'][0]['geometry']['coordinates']
            return {"lon": coords[0], "lat": coords[1]}
    except Exception as e:
        print(f"Geocoding error for {address}: {e}")
    return None

def get_travel_data(house_lat, house_lon, dest_uic_code=None):
    """
    Calculates travel duration from nearest station of a house to a destination station.
    """
    if not NS_API_KEY:
        return {"error": "NS_API_KEY not configured"}
    
    # Get closest station
    closest_station_uicCode = None
    closest_station_name = None
    closest_station = get_closest_station(house_lat, house_lon)
    if isinstance(closest_station, dict) and "error" in closest_station:
        return closest_station
    closest_station_uicCode = closest_station['closest_station_uicCode']
    closest_station_name = closest_station['station_name']
    
    # Get the next working day at 8:30am
    workday = datetime.now().replace(hour=8, minute=30)
    if workday.weekday() >= 5:  # Saturday or Sunday
        workday += timedelta(days=2 - workday.weekday())
    workday = workday.strftime("%Y-%m-%dT%H:%M:%S")

    distance_url = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips"

    headers = {
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': NS_API_KEY,
        'Content-Type': 'application/json'
    }

    params = {
        "originUicCode": closest_station_uicCode,
        "destinationUicCode": dest_uic_code,
        "dateTime": workday
    }

    try:
        response = requests.get(distance_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('trips'):
            # Extract duration in minutes from the first trip option
            time_estimate = data['trips'][0]['plannedDurationInMinutes']
            return {"duration_minutes": time_estimate, "from_station": closest_station_name}
    except Exception as e:
        return {"error": str(e)}
    
    return {"error": "No trip data found"}

def get_closest_station(house_lat, house_lon):
    if not NS_API_KEY:
        return {"error": "NS_API_KEY not configured"}

    closest_station_url = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations/nearest?lat={house_lat}&lng={house_lon}&limit=1"

    headers = {
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': NS_API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(closest_station_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract UICCode of the closest station
        closest_station = data['payload'][0]['UICCode']
        # Extract name of the station
        station_name = data['payload'][0]['namen']['lang']
        return {"closest_station_uicCode": closest_station, "station_name": station_name}
    except Exception as e:
        return {"error": str(e)}
