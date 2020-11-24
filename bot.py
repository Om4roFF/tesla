import datetime
import time
from telebot import TeleBot
from telebot import types
from AlphaCRM import customers, get_name, get_grade, is_phone, get_id_by_lesson
from database import create_table, insert, select, is_user, select_by_id, delete_from_chat
from lang_list import lang_phrases
from config import TOKEN

bot = TeleBot(TOKEN)
HTML = 'HTML'


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    try:
        if message.text == '/delete':
            delete(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Рус ' + "🇷🇺")
            markup.add('Қаз ' + "🇰🇿")
            msg = bot.send_message(message.chat.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
            bot.register_next_step_handler(msg, lang_step)
    except Exception as e:
        bot.send_message(877012379, str(e))


def lang_step(message):
    try:
        if message.text == '/start':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Рус ' + "🇷🇺")
            markup.add('Қаз ' + "🇰🇿")
            msg = bot.send_message(message.chat.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
            bot.register_next_step_handler(msg, lang_step)
        if message.text == '/delete':
            delete(message)
        lang = message.text
        lang_code = 1
        if lang == 'Рус ' + "🇷🇺":
            lang_code = 1
        elif lang == 'Қаз ' + "🇰🇿":
            lang_code = 0
        if (lang != 'Рус ' + "🇷🇺") and (lang != 'Қаз ' + "🇰🇿"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Рус ' + "🇷🇺")
            markup.add('Қаз ' + "🇰🇿")
            msg = bot.send_message(message.chat.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
            bot.register_next_step_handler(msg, lang_step)
        else:
            markup = types.ReplyKeyboardRemove()
            msg = bot.send_message(message.chat.id, lang_phrases(lang_code, 1), parse_mode=HTML, reply_markup=markup)
            bot.register_next_step_handler(msg, phone_step, lang_code)
    except Exception as e:
        bot.send_message(877012379, str(e))


def phone_step(message, lang):
    try:
        if message.text == '/start':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Рус ' + "🇷🇺")
            markup.add('Қаз ' + "🇰🇿")
            msg = bot.send_message(message.chat.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
            bot.register_next_step_handler(msg, lang_step)
        elif message.text == '/delete':
            delete(message)
        else:
            id = is_phone(message.text)
            if id:
                msg = bot.send_message(message.chat.id, lang_phrases(lang, 0), parse_mode=HTML)
                bot.register_next_step_handler(msg, grade_step, lang, id)
            else:
                msg = bot.send_message(message.chat.id, lang_phrases(lang, 2), parse_mode=HTML)
                bot.register_next_step_handler(msg, phone_step, lang)
    except Exception as e:
        bot.send_message(877012379, str(e))


def grade_step(message, lang, i_d):
    try:
        if message.text == '/start':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Рус ' + "🇷🇺")
            markup.add('Қаз ' + "🇰🇿")
            msg = bot.send_message(message.chat.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
            bot.register_next_step_handler(msg, lang_step)
        elif message.text == '/delete':
            delete(message)
        else:
            msg = bot.send_message(message.chat.id, lang_phrases(lang, 9), parse_mode=HTML)
            id = message.text
            report = []
            for m in i_d:
                if int(id) == int(m) or int(id) == int(get_id_by_lesson(id)):
                    report = get_grade(int(id))
                    print(report)
                    if not report:
                        bot.send_message(message.chat.id, (lang, 14), parse_mode=HTML)
                    else:
                        # bot.delete_message(message.chat.id, msg.message_id, timeout=5)
                        bot.send_message(message.chat.id, lang_phrases(lang, 13), parse_mode=HTML)
                        count = 0
                        customer = customers(id)
                        name = get_name(customer)
                        create_table()
                        insert(message.chat.id, m, lang, name.strip())
                        for i in report:
                            length = len(i)
                            time_from = i[1]
                            date = time_from[:10]
                            topic = i[3]
                            subject = i[2]
                            bonus = ''
                            note = ''
                            done = ''
                            tasks = ''
                            right_task = ''
                            if length == 7:
                                done = i[4]
                                bonus = i[5]
                                note = i[6]
                            elif length == 9:
                                done = i[5]
                                tasks = i[6]
                                right_task = i[4]
                                done = done + ' ' + get_percent(tasks, done)
                                right_task = right_task + ' ' + get_percent(tasks, right_task)
                                bonus = i[7]
                                note = i[8]
                            if bonus is None:
                                bonus = ''
                            if note is None:
                                note = ''

                            bot.send_message(message.chat.id,
                                             lang_phrases(lang, 12).format(name.strip(), date, subject,
                                                                           topic, tasks, done, right_task, bonus,
                                                                           note))
                            count += 1
                            if count > 3:
                                break
                # else:
                #     bot.send_message(message.chat.id, lang_phrases(lang, 6), parse_mode=HTML)
            bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.send_message(877012379, str(e))


def get_percent(full, value):
    if int(full) == 0:
        return '0 %'
    else:
        percent = (int(value) * 100) / int(full)
        return '(%.1f ' % percent + '%)'


@bot.callback_query_handler(func=lambda query: True)
def delete_step(query):
    data = query.data
    if data == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Рус ' + "🇷🇺")
        markup.add('Қаз ' + "🇰🇿")
        msg = bot.send_message(query.from_user.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        bot.register_next_step_handler(msg, lang_step)
    else:
        print(query)
        name = data
        delete_from_chat(chat_id=query.from_user.id, name=name)
        bot.send_message(query.from_user.id, 'Вы успешно отписались!')


@bot.message_handler(commands=['delete'])
def delete(message: types.Message):
    try:
        list_of_students = select_by_id(message.chat.id)
        inline = types.InlineKeyboardMarkup()
        lang = 1
        for i in list_of_students:
            lang = i[2]
            inline.add(types.InlineKeyboardButton(i[3], callback_data=str(i[3])))
        inline.add(types.InlineKeyboardButton('Назад ↵', callback_data='/start'))
        bot.send_message(message.chat.id, lang_phrases(lang, 15), reply_markup=inline)
    except Exception as e:
        bot.send_message(877012379, str(e))


if __name__ == '__main__':
    bot.polling()

