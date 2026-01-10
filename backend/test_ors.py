from distance_service import geocode_address, get_travel_data
import json

def test_distance_features():
    print("--- Testing Geocoding ---")
    address = "Dam Square, Amsterdam"
    coords = geocode_address(address)
    print(f"Geocoding '{address}': {coords}")
    
    if coords:
        print("\n--- Testing Travel Data (Driving) ---")
        travel_info = get_travel_data(coords['lat'], coords['lon'], profile='driving-car')
        print(f"Driving info: {json.dumps(travel_info, indent=2)}")
        
        print("\n--- Testing Travel Data (Cycling) ---")
        cycling_info = get_travel_data(coords['lat'], coords['lon'], profile='cycling-regular')
        print(f"Cycling info: {json.dumps(cycling_info, indent=2)}")
    else:
        print("Geocoding failed. Check your ORS_API_KEY.")

if __name__ == "__main__":
    test_distance_features()
