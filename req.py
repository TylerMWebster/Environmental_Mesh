import requests
API_KEY = "49d803595daaf36e0b096b374c15ebb7"
lat_lon = (38.443731, -78.866172)
url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat_lon[0]}&lon={lat_lon[1]}&exclude=daily,minutely&appid={API_KEY}"

def k_to_f(temp):
    return (temp - 273.15) * 1.8 + 32

print(k_to_f(requests.get(url).json()['current']['temp']))