import telebot
import logging
from telebot.types import Message
from project.CONSTS import (
    MAX_TOKENS_PER_DAY,
    API_TOKEN,
    LOGS,
    TRANSLATE,
    DEFAULT_MODEL,
    VALUES
)
from threading import Thread
from datetime import datetime
from settings_manager import load_settings, dump_settings
from weather import get_weather
from project.chat_manager import create_database, add_message, get_history, count_tokens, reset_tokens
from project.ai import ask_gpt
from project.keyboard import create_keyboard


bot = telebot.TeleBot(API_TOKEN)


def reset_users_tokens():
    reset_day = datetime.now().day
    while True:
        c_day = datetime.now().day

        if c_day != reset_day:
            reset_tokens()


def add_user(user_id):
    global settings
    settings[str(user_id)] = {'model': DEFAULT_MODEL,
                              'system_prompt': 'default'}


@bot.message_handler(commands=['start'])
def send_welcome(msg: Message):
    bot.reply_to(msg, "Привет! Я бот с нейросетью, но я также могу говорить погоду в городах. Напиши /help, "
                 "чтобы узнать список команд!")
    add_user(user_id=msg.chat.id)


@bot.message_handler(commands=['help'])
def send_help(msg: Message):
    if not settings.get(str(msg.chat.id)):
        send_welcome(msg)
        return
    bot.reply_to(msg, "Список команд:\n"
                 "/weather - узнать погоду в городе\n"
                 "/settings - настройки\n"
                 "/feedback - оставить отзыв\n")


@bot.message_handler(commands=['weather'])
def weather(msg: Message):
    user_id = msg.chat.id
    if not settings.get(str(user_id)):
        send_welcome(msg)
        return
    bot.send_message(user_id, "Хорошо! Отправь название своего города, а я отправлю тебе погоду!")
    bot.register_next_step_handler(msg, send_weather)


def send_weather(msg: Message):
    user_id = msg.chat.id
    responce, e = get_weather(msg.text)
    if e:
        bot.send_message(user_id, f'Ошибка: {e}')
    else:
        bot.send_message(user_id, responce)


@bot.message_handler(commands=['settings'])
def show_settings(msg: Message):
    user_id = msg.chat.id
    if not settings.get(str(user_id)):
        add_user(user_id)
    usr_st = ''
    for k, v in settings[str(user_id)].items():
        k = TRANSLATE[k]
        v = TRANSLATE[v] if TRANSLATE.get(v) else v
        usr_st += f'\n{k} - {v}'
    bot.send_message(user_id, f'Ваши настройки: {usr_st}', reply_markup=create_keyboard(('Изменить настройки',)))
    bot.register_next_step_handler(msg, change_settings_handler_1)


def change_settings_handler_1(msg: Message):
    user_id = msg.chat.id

    if msg.text == 'Изменить настройки':
        bot.send_message(user_id, 'Выбери, какую настройку изменить:',
                         reply_markup=create_keyboard((TRANSLATE[i] for i in settings[str(user_id)])))
        bot.register_next_step_handler(msg, change_settings_handler_2)
    else:
        handle_text(msg)


def change_settings_handler_2(msg: Message):
    user_id = msg.chat.id

    try:
        TRANSLATE[msg.text]

    except Exception as e:
        logging.info(e)
        bot.send_message(user_id, 'Что-то я не понял. Давай по новой:')
        bot.send_message(user_id, 'Выбери, какую настройку изменить:',
                         reply_markup=create_keyboard((TRANSLATE[i] for i in settings[str(user_id)])))
        bot.register_next_step_handler(msg, change_settings_handler_2)
        return

    if TRANSLATE[msg.text] in settings[str(user_id)].keys():
        bot.send_message(user_id, f'Выбери значение для параметра {msg.text}',
                         reply_markup=create_keyboard(VALUES[msg.text]))
        bot.register_next_step_handler(msg, set_settings, msg.text)


def set_settings(msg: Message, param):
    user_id = msg.chat.id

    if msg.text in VALUES[param]:
        settings[str(user_id)][TRANSLATE[param]] = msg.text
        bot.send_message(user_id, f'Значение {param} успешно заменено на {msg.text}')
        dump_settings(settings)

    else:
        bot.send_message(user_id, 'Ты написал какую-то билеберду. Давай еще раз:')
        bot.send_message(user_id, f'Выбери значение для параметра {param}',
                         reply_markup=create_keyboard(VALUES[param]))
        bot.register_next_step_handler(msg, set_settings, param)


@bot.message_handler(content_types=['text'])
def handle_text(msg: Message):
    user_id = msg.from_user.id
    if not settings.get(str(user_id)):
        send_welcome(msg)
        return
    if msg.text[0] == '/':
        bot.send_message(user_id, "К сожалению, такой команды у нас еще нет. Вот список команд:\n"
                         "/weather - узнать погоду в городе\n"
                         "/settings - настройки\n"
                         "/feedback - оставить отзыв\n")
        return

    if count_tokens(user_id) >= MAX_TOKENS_PER_DAY:
        bot.send_message(user_id, 'Извините, бесплатные токены на сегодня закончились, '
                                  'но они начислятся в 00:00 по Москве!')
        return

    add_message(user_id, (msg.text, 'user', 0))
    chat_history = get_history(user_id)

    status, answer, answer_tokens = ask_gpt(chat_history, settings[str(user_id)]['model'],
                                            settings[str(user_id)]['system_prompt'])

    if status:
        bot.send_message(user_id, answer + f"\n(Потрачено токенов: {answer_tokens})")
        add_message(user_id, (answer, 'assistant', answer_tokens))
    else:
        bot.send_message(user_id, 'Извините, что-то пошло не так')


if __name__ == '__main__':
    Thread(target=reset_users_tokens).start()
    settings = load_settings()
    create_database()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H",
        filename=LOGS,
        filemode="a",
        encoding="utf-8",
        force=True)
    bot.infinity_polling()
