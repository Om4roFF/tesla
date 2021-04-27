import datetime
import time
from telebot import TeleBot
from telebot import types
from alpha_crm_grade import get_grade
from alpha_crm_lesson import get_id_by_lesson
from alpha_crm_phone import is_phone
from alpha_crm_customer import customers
from database import create_table, insert, select_by_id, delete_from_chat
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
        print(e)


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
        else:
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
        print(e)


def phone_step(message, lang):
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Рус ' + "🇷🇺")
        markup.add('Қаз ' + "🇰🇿")
        msg = bot.send_message(message.chat.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        bot.register_next_step_handler(msg, lang_step)
    elif message.text == '/delete':
        delete(message)
    else:
        ids = []
        try:
            ids = is_phone(message.text)
        except Exception as e:
            print(e)
            ids = is_phone(message.text)
            print(ids)
        if ids:
            msg = bot.send_message(message.chat.id, lang_phrases(lang, 0), parse_mode=HTML)
            bot.register_next_step_handler(msg, student_step, lang, ids)
        else:
            msg = bot.send_message(message.chat.id, lang_phrases(lang, 2), parse_mode=HTML)
            bot.register_next_step_handler(msg, phone_step, lang)


def student_step(message, lang, i_d):
    # try:
        if message.text == '/start':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Рус ' + "🇷🇺")
            markup.add('Қаз ' + "🇰🇿")
            msg = bot.send_message(message.chat.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
            bot.register_next_step_handler(msg, lang_step)
        elif message.text == '/delete':
            delete(message)
        else:
            id = message.text
            print(id)
            print(i_d)
            for m in i_d:
                is_lesson_id = ''
                print('m', m)
                try:
                    print('in lesson_id')
                    is_lesson_id = get_id_by_lesson(id)
                except Exception as e:
                    bot.send_message(877012379, 'lesson_id' + str(e))
                    is_lesson_id = get_id_by_lesson(id)
                if int(id) == int(m) or int(id) == int(is_lesson_id):
                    print('verification')
                    customer = ''
                    try:
                        customer = customers(id)
                    except Exception as e:
                        bot.send_message(877012379, 'customer' + str(e))
                        customer = customers(id)
                    name = get_name(customer)
                    print(name)
                    create_table()
                    insert(message.chat.id, id, lang, name.strip())
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(lang_phrases(lang, 4))
                    markup.add(lang_phrases(lang, 5))
                    msg = bot.send_message(message.chat.id, text=lang_phrases(lang, 3).format(name), reply_markup=markup, parse_mode=HTML)
                    bot.register_next_step_handler(msg, grade_step, name, id, lang, i_d)
                    break
    # except Exception as e:
    #     bot.send_message(877012379, 'student_step end ' + str(e))


def grade_step(message, name, i_d, lang, ids):
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Рус ' + "🇷🇺")
        markup.add('Қаз ' + "🇰🇿")
        msg = bot.send_message(message.chat.id, text=lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        bot.register_next_step_handler(msg, lang_step)
    elif message.text == '/delete':
        delete(message)
    elif message.text == lang_phrases(lang, 4):
        markup = types.ReplyKeyboardRemove()
        msg = bot.send_message(message.chat.id, lang_phrases(lang, 9), parse_mode=HTML, reply_markup=markup)
        report = []
        try:
            report = get_grade(int(i_d))
        except Exception as e:
            print(e)
            time.sleep(4)
            report = get_grade(int(i_d))
        if not report:
            bot.send_message(message.chat.id, lang_phrases(lang, 14), parse_mode=HTML)
        else:
            bot.send_message(message.chat.id, lang_phrases(lang, 13), parse_mode=HTML)
            count = 0
            for lesson in report:
                time_from = lesson.date
                date = time_from[:10]
                topic = lesson.topic
                subject = lesson.subject
                bonus = lesson.bonus
                note = lesson.note
                grade = lesson.grade
                if bonus is None:
                    bonus = ''
                if note is None:
                    note = ''
                bot.send_message(message.chat.id,
                                 lang_phrases(lang, 12).format(name.strip(), date, subject,
                                                               topic, grade, bonus,
                                                               note))
                count += 1
                if count > 2:
                    break
        bot.delete_message(message.chat.id, msg.message_id)
    elif message.text == lang_phrases(lang, 5):
        msg = bot.send_message(message.chat.id, lang_phrases(lang, 0), parse_mode=HTML)
        bot.register_next_step_handler(msg, student_step, lang, ids)


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
        bot.send_message(message.chat.id, lang_phrases(lang, 15), reply_markup=inline)
    except Exception as e:
        bot.send_message(877012379, 'delete' + str(e))


def get_name(text):
    customer_list = text.split(',')
    s = customer_list[3]
    s = s.split(':')
    name = s[1]
    name = name.replace("'", " ")
    return name


if __name__ == '__main__':
    bot.polling()

