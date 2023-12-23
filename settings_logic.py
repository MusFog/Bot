from telebot import types
from start_logic import ask_for_settings, start_logic
from utils import save_user_id
from language.language import translations
from utils import load_user_ids

def settings_logic(user_id, message, bot):
    user_ids = load_user_ids()
    language_choice = user_ids.get(user_id, "English")  

    text = translations[language_choice]["choose_setting"]
    save_setting = translations[language_choice]["save_setting"]

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🌐 Language", callback_data="language_settings")
    btn_back = types.InlineKeyboardButton(text=save_setting, callback_data="back_to_menu")
    markup.add(btn1, btn_back)
    bot.send_message(message.chat.id, text, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == "language_settings")
    def language_settings(call):
        user_ids = load_user_ids()
        language_choice = user_ids.get(user_id, "English")

        text = translations[language_choice]["choose_language"]

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("🇺🇦 Українська", callback_data="Ukrainian")
        btn2 = types.InlineKeyboardButton("🇬🇧 English", callback_data="English")
        markup.add(btn1, btn2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data in ["Ukrainian", "English"])
    def handle_language_choice(call):
        language = call.data
        save_user_id(user_id, language)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        settings_logic(user_id, message, bot)
    @bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
    def back_to_menu(call):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        ask_for_settings(message, bot, settings_logic)  
        


