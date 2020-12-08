import json
import telebot
import config
import json
import threading
from datetime import *
import time
import logging

bot = telebot.TeleBot(config.TOKEN)

with open("users.json", encoding="utf-8") as js:
    users_data = json.load(js)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Вітаю {message.from_user.first_name}!\n"
                                      f"Я <b>{bot.get_me().first_name}</b>,"
                                      f" бот який сповіщує працівника про початок роботи. "
                                      f"\nНапиши /set_time щоб встановити час сповіщень"
                                      f"\nНапиши /set_role щоб встановити свою роль в компанії"
                                      f"\nНапиши /help для перегляду доступних команд.",
                                      parse_mode='html')

    users_data[f"{message.chat.id}"] = {"time": "", "role": ""}

    with open('users.json', 'w', encoding="utf-8") as js:
        json.dump(users_data, js)

@bot.message_handler(commands=["help"])
def show_commands(message):
    bot.send_message(message.chat.id, "/start - Початок роботи"
                                      "\n/set_time - Встановити час"
                                      "\n/set_role - Встановити роль"
                                      "\n/help - Показати доступні команди"
                                      "\n/leave - Вимкнути сповіщення")
