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

@bot.message_handler(commands=["set_time"])
def set_time(message):
    if str(message.chat.id) in users_data:
        bot.send_message(message.chat.id, "Напишіть час у форматі HH:MM")
        bot.register_next_step_handler(message, time_setting)
    else:
        bot.send_message(message.chat.id, "Вас немає у списку користувачів!")

        def time_setting(message):
            users_data[f"{message.chat.id}"]["time"] = message.text + ":00"

            with open('users.json', 'w', encoding="utf-8") as js:
                json.dump(users_data, js)

            bot.send_message(message.chat.id, "Час успішно збережено")

            @bot.message_handler(commands=["set_role"])
            def set_role(message):
                if str(message.chat.id) in users_data:
                    bot.send_message(message.chat.id, "Напишіть свою роль в компанії")
                    bot.register_next_step_handler(message, role_setting)
                else:
                    bot.send_message(message.chat.id, "Вас немає у списку користувачів!")

            def role_setting(message):
                users_data[f"{message.chat.id}"]["role"] = message.text

                with open("users.json", "w", encoding="utf-8") as js:
                    json.dump(users_data, js)

                bot.send_message(message.chat.id, "Роль успішно збережено")


                @bot.message_handler(commands=["leave"])
                def leave(message):
                    if str(message.chat.id) in users_data:
                        users_data.pop(str(message.chat.id))

                        with open('users.json', 'w', encoding="utf-8") as js:
                            json.dump(users_data, js)

                        bot.send_message(message.chat.id, "Ви успішно вимкнули сповіщення. "
                                                          "\nЩоб ввімкнути сповіщення напишіть \n/start, /set_time, /set_role")
                    else:
                        bot.send_message(message.chat.id, "Вас немає у списку користувачів!")