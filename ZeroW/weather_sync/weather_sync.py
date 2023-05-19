import requests

WEATHER_API_KEY = open('weatherapi.key' ,'r').read()

def update_weather():
    data = requests.get(f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Caan&aqi=no')
    j = data.json()
    temp_c = j.get('current').get('temp_c')
    # is_day = j.get('current').get('is_day')
    condition = j.get('current').get('condition').get('text')
    wind_kph = j.get('current').get('wind_kph')
    humidity = j.get('current').get('humidity')
    weatherstr = f'''Today's weather in Caan:
Condition:  {condition}
Temp:       {temp_c}C
Humidity:   {humidity}%
Wind:       {wind_kph}km/h'''
    # with open('weather.tmp', 'w') as f:
    #     f.write(weatherstr)
    #     f.close()
    return weatherstr
