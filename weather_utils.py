import requests
from utils import save_user_id, load_user_ids
from language.language import translations 

def get_weekly_weather(user_id, lat, lon, appid):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={appid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return format_weather_message(user_id, weather_data)
    except requests.RequestException as e:
        return f"Error getting weather data: {e}"


def format_weather_message(user_id, weather_data):
    message_lines = []
    user_ids = load_user_ids()
    language_choice = user_ids.get(user_id, "English") 
    translations_dict = translations[language_choice]

    current_weather = weather_data['list'][0]
    description = current_weather['weather'][0]['description']
    wind_speed = current_weather['wind']['speed']
    humidity = current_weather['main']['humidity']
    pressure = current_weather['main']['pressure']
    temperature2 = translations[language_choice]["temperature2"]
    status = translations[language_choice]["status"]
    wind_speed2 = translations[language_choice]["wind_speed2"]
    current_weather = weather_data['list'][0]  
    temperature = current_weather['main']['temp'] - 273.15  
    description = current_weather['weather'][0]['description']
    wind_speed = current_weather['wind']['speed']
    icon_code = current_weather['weather'][0]['icon']

    icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

    message_lines.append(f"{temperature2}: {temperature:.2f}°C")
    message_lines.append(f"{status}: {description.capitalize()}")
    message_lines.append(f"🌬️ {wind_speed2}: {wind_speed} m/s")
    message_lines.append(f"💧 {translations_dict['humidity']}: {humidity}%")
    message_lines.append(f"🔵 {translations_dict['pressure']}: {pressure} hPa")
    message_lines.append(f"🔗 {icon_url}")


    return "\n".join(message_lines)
def countries_cities(message, user_id):
    user_ids = load_user_ids()
    language_choice = user_ids.get(user_id, "English") 
    countries_cities_translated = translations[language_choice]["countries_cities"]
    return countries_cities_translated


