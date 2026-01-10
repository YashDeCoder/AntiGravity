from distance_service import geocode_address, get_travel_data
import json

def test_specific_address():
    address = "Bankierbaan 234"
    print(f"--- Testing Address: {address} ---")
    
    # 1. Geocode the address
    coords = geocode_address(address)
    print(f"Coordinates: {coords}")
    
    if coords:
        # 2. Get travel data to Bijlmer ArenA
        travel_info = get_travel_data(coords['lat'], coords['lon'])
        print(f"Travel Info: {json.dumps(travel_info, indent=2)}")
    else:
        print("Geocoding failed.")

if __name__ == "__main__":
    test_specific_address()
