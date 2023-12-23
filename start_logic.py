from telebot import types
from main_menu import main_menu
from utils import save_user_id, load_user_ids
from language.language import translations 
from telebot.types import ReplyKeyboardRemove

def start_logic(message, bot, settings_logic):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    user_ids = load_user_ids()

    if user_id in user_ids:
        ask_for_settings(message, bot, settings_logic)
        return
    settings_logic(user_id, message, bot)

def ask_for_settings(message, bot, settings_logic):
    user_id = message.from_user.id
    user_ids = load_user_ids()
    language_choice = user_ids.get(user_id, "English")

    current_language_text = translations[language_choice]["current_language"].format(language_choice)
    text = translations[language_choice]["settings"] + "\n\n" + current_language_text
    yes_text = translations[language_choice]["yes"]
    no_text = translations[language_choice]["no"]
    saved = translations[language_choice]["saved"]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(yes_text)
    btn2 = types.KeyboardButton(no_text)
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text, reply_markup=markup)
    

    @bot.message_handler(func=lambda message: message.text == no_text)
    def handle_no_response(message):
        bot.delete_message(message.chat.id, message.message_id)
        settings_no = bot.send_message(message.chat.id, ".", reply_markup=ReplyKeyboardRemove())
        settings_no_id = settings_no.message_id
        bot.delete_message(message.chat.id, settings_no_id)
        settings_logic(user_id, message, bot)

    @bot.message_handler(func=lambda message: message.text == yes_text)
    def handle_yes_response(message):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, saved, reply_markup=ReplyKeyboardRemove())
        main_menu(user_id, message, bot, settings_logic)

