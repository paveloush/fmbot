# -*- coding: utf-8 -*-
import random

import datetime
import telebot
import time
from telebot import types

token = ''
regex_exception = r"(dicegame\.io)"
regex_url = r"(https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?"
blocktime = 60

bot = telebot.TeleBot(token)


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)

@bot.message_handler(content_types=['text'], regexp=regex_exception)
def handle_message(message):
    pass


# Delete URLs in groups
@bot.message_handler(content_types=['text'], regexp=regex_url)
def handle_message(message):
    if message.chat.type == 'supergroup':
        # bot.send_message(message.chat.id, 'it\'s an URL!')
        bot.delete_message(message.chat.id, message.message_id)
        bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time() + blocktime)


# Greeting new group's members and send ID to private chat
@bot.message_handler(content_types=['new_chat_members'])
def handle_message(message):
    name = message.new_chat_members[-1].first_name
    user_id = message.new_chat_members[-1].id

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Click here to get a code",
                                         url="https://telegram.me/testfmbot?start=test")
    markup.add(button1)
    bot.send_message(chat_id=message.chat.id, text='Welcome, ' + name + '!', reply_markup=markup)

    with open('list.txt', 'a') as l:
        l.write('%s %s %s \n' % (user_id, datetime.date.today(), name))

        # # sending private message to user with his ID:
        # user_id = message.new_chat_members[-1].id
        # bot.send_message(user_id, 'Hey, {}! Here\'s your code:'.format(message.new_chat_members[-1].first_name))
        # bot.send_message(user_id, user_id)


@bot.message_handler(content_types=['left_chat_member'])
def handle_message(message):
    user_id = message.left_chat_member.id
    with open('list.txt', 'r+') as f:
        lines = f.readlines()
    with open('list.txt', 'w') as f:
        for line in lines:
            if line.find(str(user_id)) != 0:
                f.write(line)


# send id in private chat after command /get_code and /start
@bot.message_handler(commands=['code', 'start'])
def handle_start_help(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, 'Copy following code to the form:')
        bot.send_message(message.chat.id, message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        keybutton1 = types.KeyboardButton(text="Roll the dice")
        keybutton2 = types.KeyboardButton(text="Menu")
        keybutton3 = types.KeyboardButton(text="Get a code again")
        keyboard.add(keybutton1, keybutton2, keybutton3)
        bot.send_message(message.chat.id, "Choose action:", reply_markup=keyboard)


### COMMANDS WITHOUT /
@bot.message_handler(func=lambda message: message.text == 'Menu' and message.content_type == 'text')
def handle_start_help(message):
    if message.chat.type == 'private':
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keybutton1 = types.KeyboardButton(text="About")
        keybutton2 = types.KeyboardButton(text="How to")
        keybutton3 = types.KeyboardButton(text="<Back<")
        keyboard.add(keybutton1, keybutton2, keybutton3)
        bot.send_message(message.chat.id, "Menu:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Roll the dice' and message.content_type == 'text')
def roll_dice(message):
    emoji_list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣']
    emoji = random.choice(emoji_list)
    bot.send_message(message.chat.id, emoji)


@bot.message_handler(func=lambda message: message.text == 'Get a code again' and message.content_type == 'text')
def switch(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Copy following code to the form:')
    bot.send_message(user_id, user_id)


@bot.message_handler(func=lambda message: message.text == 'About' and message.content_type == 'text')
def switch(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Multiple string text about project.\nMultiple string text about project.')


@bot.message_handler(func=lambda message: message.text == 'How to' and message.content_type == 'text')
def switch(message):
    user_id = message.from_user.id
    head = "**HOW TO PLAY:**\r\n\r\n• Paragraph 1\r\n• Paragraph 2\r\n• Paragraph 3"
    bot.send_message(user_id, head)


@bot.message_handler(func=lambda message: message.text == '<Back<' and message.content_type == 'text')
def handle_start_help(message):
    if message.chat.type == 'private':
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keybutton1 = types.KeyboardButton(text="Roll the dice")
        keybutton2 = types.KeyboardButton(text="Menu")
        keybutton3 = types.KeyboardButton(text="Get a code again")
        keyboard.add(keybutton1, keybutton2, keybutton3)
        bot.send_message(message.chat.id, "Choose action", reply_markup=keyboard)


###END COMMANDS


# roll the dice after command /dice
@bot.message_handler(commands=['dice'])
def roll_dice(message):
    emoji_list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣']
    emoji = random.choice(emoji_list)
    bot.send_message(message.chat.id, emoji)


# @bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])

# delete edited messages with URLs
@bot.edited_message_handler(func=lambda message: True, content_types=['text'], regexp=regex_url)
def edit_message(message):
    if message.chat.type == 'supergroup':
        bot.delete_message(message.chat.id, message.message_id)


# message.from_user.id

@bot.message_handler(commands=['switch'])
def switch(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Copy following code to the form:')
    bot.send_message(user_id, user_id)


# @bot.message_handler(commands=['faq'])
# def default_test(message):
#     keyboard = types.InlineKeyboardMarkup()
#     url_button1 = types.InlineKeyboardButton(text="ссылка1", url="https://ya.ru")
#     url_button2 = types.InlineKeyboardButton(text="ссылка2", url="https://vk.com")
#     url_button3 = types.InlineKeyboardButton(text="ссылка3", url="https://tut.by")
#     keyboard.add(url_button1, url_button2, url_button3)
#     bot.send_message(message.chat.id, "Привет! Choose the button", reply_markup=keyboard)
#
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = telebot.types.InlineKeyboardMarkup()
#     button1 = telebot.types.InlineKeyboardButton(text='menu2', callback_data='menu2')
#     button2 = telebot.types.InlineKeyboardButton(text='faq', callback_data='faq')
#     markup.add(button1, button2)
#     bot.send_message(chat_id=message.chat.id, text='Some text', reply_markup=markup)


@bot.message_handler(commands=['menu'])
def main_menu(message):
    main_markup = types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text='About', callback_data='about')
    button2 = telebot.types.InlineKeyboardButton(text='How to', callback_data='ht')
    button3 = telebot.types.InlineKeyboardButton(text='Commands', callback_data='commands')
    main_markup.add(button1, button2, button3)
    msg = bot.send_message(chat_id=message.chat.id, text='Main menu', reply_markup=main_markup)


@bot.callback_query_handler(func=lambda call: True)
def inline(c):
    if c.data == 'about':
        about_markup = types.InlineKeyboardMarkup()
        about_markup.add(types.InlineKeyboardButton(text='<<<Hазад', callback_data='back'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="About:",
            parse_mode="markdown",
            reply_markup=about_markup)
    elif c.data == 'ht':
        about_markup = types.InlineKeyboardMarkup()
        about_markup.add(types.InlineKeyboardButton(text='<<<Hазад', callback_data='back'))
        head = "*HOW TO PLAY:* \r\n\r\n• Paragraph 1\r\n• Paragraph 2\r\n• Paragraph 3"
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=head,
            parse_mode="markdown",
            reply_markup=about_markup)
    elif c.data == 'commands':
        about_markup = types.InlineKeyboardMarkup()
        about_markup.add(types.InlineKeyboardButton(text='<<<Hазад', callback_data='back'))
        head = "*Bots commands:* \r\n\r\n• /code - receive your personal code\r\n• _Wow!_\r\n• _So telegram!_" \
               "\r\n• /dice - roll the dice"
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=head,
            parse_mode="markdown",
            reply_markup=about_markup)
    elif c.data == 'back':
        main_markup = types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text='About', callback_data='about')
        button2 = telebot.types.InlineKeyboardButton(text='How to', callback_data='ht')
        button3 = telebot.types.InlineKeyboardButton(text='Commands', callback_data='commands')
        main_markup.add(button1, button2, button3)
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text='Main menu:',
            parse_mode="markdown",
            reply_markup=main_markup)
    elif c.data == 'click':
        main_markup = types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text='About', callback_data='about')
        button2 = telebot.types.InlineKeyboardButton(text='How to', callback_data='ht')
        button3 = telebot.types.InlineKeyboardButton(text='Commands', callback_data='commands')
        main_markup.add(button1, button2, button3)
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text='Main menu:',
            parse_mode="markdown",
            reply_markup=main_markup)


while True:
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True)

    # ConnectionError and ReadTimeout because of possible timout of the requests library
    # TypeError for moviepy errors
    # maybe there are others, therefore Exception

    except Exception as e:
        telebot.logger.error(e)
        time.sleep(10)
