import requests
import urllib.parse

TOMTOM_API_KEY = "AQC32Ji96lt815SPIrptJWeOBYsLuDcv"

def geocode_location(location_name):
    

    location_encoded = urllib.parse.quote(location_name)
    url = f"https://api.tomtom.com/search/2/geocode/{location_encoded}.json"
    params = {
        "key": TOMTOM_API_KEY,
        "limit": 1
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        print("GEOCODE URL:", resp.url)
        print("STATUS:", resp.status_code)
        print("TEXT:", resp.text)

        if resp.status_code == 200:
            data = resp.json()
            if data["results"]:
                lat = data["results"][0]["position"]["lat"]
                lon = data["results"][0]["position"]["lon"]
                return lat, lon
            else:
                return None, None
        else:
            return None, None

    except Exception as e:
        print("Geocoding error:", e)
        return None, None


def fetch_traffic_data(lat, lon):
   

    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"
    params = {
        "point": f"{lat},{lon}",
        "key": TOMTOM_API_KEY
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        print("TRAFFIC URL:", resp.url)
        print("STATUS:", resp.status_code)
        print("TEXT:", resp.text)

        if resp.status_code == 200:
            data = resp.json()
            if "flowSegmentData" in data:
                return data["flowSegmentData"]
            else:
                return None
        else:
            return None

    except Exception as e:
        print("Traffic error:", e)
        return None
