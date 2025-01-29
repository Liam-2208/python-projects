import requests
import datetime

url = "https://api.openweathermap.org/data/2.5/forecast?lat=51.4545&lon=-2.5879&appid=ed6e46132ac15dc55afcd970de4e1a37&units=metric"
response = requests.get(url)

if response.status_code == 200:
    print("Request successful!")
    data = response.json()
else:
    print(f"Error: {response.status_code}")

for i in data['list']:
    print(f"datetime: {datetime.datetime.fromtimestamp(i['dt'])}")
    print(f"main: {i['main']}")
    print(f"weather: {i['weather']}")
    print(f"clouds: {i['clouds']}")
    print(f"wind: {i['wind']}")
    print("\n")
