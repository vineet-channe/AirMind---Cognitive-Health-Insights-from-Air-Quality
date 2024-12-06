import requests

API_KEY = "ce0811ef8af98caff128eb17a7c20b00"  # Replace with your OpenWeatherMap API Key

def get_air_quality_data(lat, lon):
    """
    Fetches air quality data for the given latitude and longitude from OpenWeatherMap API.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        dict: Air quality data with necessary components, or None if data is unavailable.
    """
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Debugging: Check the raw response
    print("Raw API Response:", data)

    # Extract and validate data
    if 'list' in data and len(data['list']) > 0:
        try:
            air_quality_data = {
                "pm2_5": data['list'][0]['components']['pm2_5'],
                "pm10": data['list'][0]['components']['pm10'],
                "co": data['list'][0]['components']['co'],
                "no2": data['list'][0]['components']['no2'],
                "so2": data['list'][0]['components']['so2'],
                "o3": data['list'][0]['components']['o3'],
            }
            return air_quality_data
        except KeyError as e:
            print(f"KeyError in parsing air quality data: {e}")
            return None
    else:
        print("No 'list' key or data in API response")
        return None
