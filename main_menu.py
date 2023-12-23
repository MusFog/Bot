from telebot import types
import telebot
from language.language import translations
from utils import load_user_ids
from weather_utils import countries_cities

user_states = {}  
main_menu_ids = {}
last_city_message_id = None
last_country_message_id = None
last_back_to_main_menu_id = None

def main_menu(user_id, message, bot, settings_logic):
    user_ids = load_user_ids()
    language_choice = user_ids.get(user_id, "English")
    if user_id in main_menu_ids:
        try:
            bot.delete_message(message.chat.id, main_menu_ids[user_id])
        except telebot.apihelper.ApiTelegramException:
            pass
    settings_button = translations[language_choice]["settings_button"]
    help_button = translations[language_choice]["help_button"]
    weather_button = translations[language_choice]["weather_button"]
    choose_country = translations[language_choice]["choose_country"]
    err_choose_country = translations[language_choice]["err_choose_country"]  
    select_city = translations[language_choice]["select_city"]  
    support_here = translations[language_choice]["support_here"]  
    you_wrote = translations[language_choice]["you_wrote"] 
    menu = translations[language_choice]["menu"]
    support_here_back = translations[language_choice]["support_here_back"]
    back_to_main_menu = translations[language_choice]["back_to_main_menu"]

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=f"⚙️ {settings_button}", callback_data="settings")
    btn2 = types.InlineKeyboardButton(text=f"❓ {help_button}", callback_data="help")
    btn3 = types.InlineKeyboardButton(text=f"🌤️ {weather_button}", callback_data="weather")

    markup.add(btn1, btn2, btn3) 
    
    menu = bot.send_message(message.chat.id, menu, reply_markup=markup)
    main_menu_ids[user_id] = menu.message_id

    @bot.callback_query_handler(func=lambda call: call.data == "weather")
    def handle_weather_button(call):
        global last_country_message_id, last_city_message_id

        if last_city_message_id:
            try:
                bot.delete_message(call.message.chat.id, last_city_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_city_message_id = None

        if last_country_message_id:
            try:
                bot.delete_message(call.message.chat.id, last_country_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_country_message_id = None
        if user_id in user_states:
            try:
                bot.delete_message(call.message.chat.id, user_states[user_id])
            except telebot.apihelper.ApiTelegramException:
                pass  

    
        countries_cities_dict = countries_cities(call.message, user_id)  

        markup = types.InlineKeyboardMarkup()
        for country in countries_cities_dict.keys():
            markup.add(types.InlineKeyboardButton(text=country, callback_data=f"country_{country}"))
        sent_message = bot.send_message(call.message.chat.id, choose_country, reply_markup=markup)
        last_country_message_id = sent_message.message_id


    @bot.callback_query_handler(func=lambda call: call.data.startswith("country_"))
    def handle_country_selection(call):
        global last_city_message_id

        if last_city_message_id:
            try:
                bot.delete_message(call.message.chat.id, last_city_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_city_message_id = None
        
        if user_id in user_states:
            try:
                bot.delete_message(call.message.chat.id, user_states[user_id])
            except telebot.apihelper.ApiTelegramException:
                pass  

        selected_country = call.data.split("_")[1]
        countries_cities_dict = countries_cities(call.message, user_id)  
        if selected_country in countries_cities_dict:
            markup = types.InlineKeyboardMarkup()
            for city_name in countries_cities_dict[selected_country].keys():
                markup.add(types.InlineKeyboardButton(text=city_name, callback_data=f"weather_{city_name}"))
            sent_message = bot.send_message(call.message.chat.id, select_city, reply_markup=markup)
            last_city_message_id = sent_message.message_id
        else:
            bot.send_message(call.message.chat.id, err_choose_country)

    @bot.callback_query_handler(func=lambda call: call.data == "settings")
    def handle_settings_button(call):
        global last_country_message_id, last_city_message_id, main_menu_ids, last_back_to_main_menu_id

       
        if user_id in main_menu_ids:
            try:
                bot.edit_message_reply_markup(call.message.chat.id, main_menu_ids[user_id], reply_markup=None)
            except telebot.apihelper.ApiTelegramException:
                pass

        if last_country_message_id:
            try:
                bot.delete_message(call.message.chat.id, last_country_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_country_message_id = None

        if last_city_message_id:
            try:
                bot.delete_message(call.message.chat.id, last_city_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_city_message_id = None
        if user_id in user_states:
            try:
                bot.delete_message(call.message.chat.id, user_states[user_id])
            except telebot.apihelper.ApiTelegramException:
                pass
        settings_logic(user_id, message, bot)


    @bot.callback_query_handler(func=lambda call: call.data == "help")
    def handle_help_button(call):
        global last_country_message_id, last_city_message_id, main_menu_ids, last_back_to_main_menu_id


       
        if user_id in main_menu_ids:
            try:
                bot.edit_message_reply_markup(call.message.chat.id, main_menu_ids[user_id], reply_markup=None)
            except telebot.apihelper.ApiTelegramException:
                pass

        if last_country_message_id:
            try:
                bot.delete_message(call.message.chat.id, last_country_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_country_message_id = None

        if last_city_message_id:
            try:
                bot.delete_message(call.message.chat.id, last_city_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_city_message_id = None
        if user_id in user_states:
            try:
                bot.delete_message(call.message.chat.id, user_states[user_id])
            except telebot.apihelper.ApiTelegramException:
                pass    

        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(text=back_to_main_menu, callback_data="back_to_main_menu")
        markup.add(back_button)
        send_message_id = bot.send_message(call.message.chat.id, support_here_back, reply_markup=markup)
        last_back_to_main_menu_id = send_message_id.message_id
        if not isinstance(user_states.get(user_id), dict):
            user_states[user_id] = {}
        user_states[user_id]['message_help'] = "AWAITING_USER_MESSAGE"



    @bot.callback_query_handler(func=lambda call: call.data == "back_to_main_menu")
    def handle_back_to_main_menu(call):
        global last_back_to_main_menu_id, user_states

        if user_id not in user_states:
            user_states[user_id] = {}
        if last_back_to_main_menu_id:
            try:
                bot.delete_message(call.message.chat.id, last_back_to_main_menu_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_back_to_main_menu_id = None
        if user_id in user_states and 'message_help' in user_states[user_id]:
            del user_states[user_id]['message_help']
        main_menu(user_id, message, bot, settings_logic) 


    @bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('message_help') == "AWAITING_USER_MESSAGE")
    def handle_user_message(message):
        bot.send_message(message.chat.id, f"{you_wrote}: {message.text}")
        global last_back_to_main_menu_id

        if last_back_to_main_menu_id:
            try:
                bot.delete_message(message.chat.id, last_back_to_main_menu_id)
            except telebot.apihelper.ApiTelegramException:
                pass
            last_back_to_main_menu_id = None

        main_menu(user_id, message, bot, settings_logic)

        if user_id in user_states and 'message_help' in user_states[user_id]:
            del user_states[user_id]['message_help']