import telebot
from start_logic import start_logic
from settings_logic import settings_logic
from utils import load_user_ids
from weather_utils import countries_cities
from weather_utils import get_weekly_weather
from main_menu import user_states

bot_token = "####################################"
bot = telebot.TeleBot(bot_token)


user_ids = load_user_ids()

@bot.message_handler(commands=['start'])
def start(message):
    start_logic(message, bot, settings_logic)


@bot.message_handler(commands=['settings'])
def handle_settings_command(message):
    settings_logic(message, bot)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("weather_"))
def handle_city_weather(call):
    user_id = call.from_user.id
    countries_cities_dict = countries_cities(call.message, user_id)
    city_name = call.data.split("_")[1]
    city_coords = None

    for country, cities in countries_cities_dict.items():
        if city_name in cities:
            city_coords = cities[city_name]
            break

    if city_coords:
        user_id = call.from_user.id
        weather_info = get_weekly_weather(user_id, city_coords['lat'], city_coords['lon'], 'c9aa0b49abc9a6479445768eb71567a4')
        if user_id in user_states:
            try:
                bot.delete_message(call.message.chat.id, user_states[user_id])
            except telebot.apihelper.ApiTelegramException:
                pass

        sent_message = bot.send_message(call.message.chat.id, weather_info)

        user_states[user_id] = sent_message.message_id
    else:
        bot.send_message(call.message.chat.id, "An error occurred while selecting the city.")



bot.polling(none_stop=True, interval=0)