import datetime
import time

from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from AlphaCRM import customers, get_name, get_grade, is_phone, get_id_by_lesson
from database import create_table, insert, select, is_user, select_by_id, delete_from_chat
from next_step import States
import asyncio
from lang_list import lang_phrases
from config import TOKEN

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
HTML = types.ParseMode.HTML


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
    markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
    await message.answer(
        text=lang_phrases(1, 10),
        reply_markup=markup, parse_mode=HTML)
    await States.lang.set()


@dp.callback_query_handler(state=States.lang)
async def lang_step(query: types.CallbackQuery, state: FSMContext):
    message = query.message
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await message.answer(lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()
    if message.text == '/delete':
        await delete(message)
    lang = query.data
    lang_code = 0
    if lang == 'Рус':
        await state.update_data(lang=1)
        lang_code = 1
    elif lang == 'Қаз':
        await state.update_data(lang=0)
    elif lang == 'again':
        data = await state.get_data()
        lang_code = data.get('lang')
        if lang_code == 1:
            lang = 'Рус'
        if lang_code == 0:
            lang = 'Қаз'
    if (lang != 'Рус') and (lang != 'Қаз'):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await message.answer(lang_phrases(lang, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()
    else:
        await message.answer(lang_phrases(lang_code, 1), parse_mode=HTML)
        await States.phone.set()


@dp.message_handler(state=States.phone)
async def phone_step(message: types, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await message.answer(lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()
    elif message.text == '/delete':
        await delete(message)
    else:
        id = await is_phone(message.text)
        print(id)
        await state.update_data(id=id)
        if id:
            print('in id')
            await message.answer(lang_phrases(lang, 0), parse_mode=HTML)
            await States.id.set()
        else:
            await message.answer(lang_phrases(lang, 2), parse_mode=HTML)
            await States.phone.set()


@dp.message_handler(state=States.id)
async def id_step(message: types.Message, state: FSMContext):
    print('id step')
    data = await state.get_data()
    lang = data.get('lang')
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await message.answer(lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()
    elif message.text == '/delete':
        await delete(message)
    else:
        id = message.text
        i_d = data.get('id')
        id2 = await get_id_by_lesson(int(id))
        if int(id) == int(i_d) or int(id) == int(id2):
            customer = await customers(id)
            name = ''
            try:
                name = await get_name(customer)
            except Exception as e:
                await bot.send_message(877012379, 'id_step ' + str(e))
            await state.update_data(name=name)
            await state.update_data(id=id)
            create_table()
            insert(message.chat.id, id, lang, name.strip())
            inline_markup = types.InlineKeyboardMarkup()
            inline_markup.add(types.InlineKeyboardButton(lang_phrases(lang, 4), callback_data='da'))
            inline_markup.add(types.InlineKeyboardButton(lang_phrases(lang, 5), callback_data='net'))
            await message.answer(lang_phrases(lang, 3).format(str(name)), reply_markup=inline_markup, parse_mode=HTML)
            await States.grade.set()
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(lang_phrases(lang, 7), callback_data='again'))
            await message.answer(lang_phrases(lang, 8), parse_mode=HTML, reply_markup=markup)
            await States.lang.set()


@dp.callback_query_handler(state=States.grade)
async def grade_step(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    name = data.get('name')
    if query.data == 'da':
        await query.message.answer(lang_phrases(lang, 13), parse_mode=HTML)
        msg = await query.message.answer(lang_phrases(lang, 9), parse_mode=HTML)
        data = await state.get_data()
        id = data.get('id')
        report = await get_grade(int(id))
        await msg.delete()
        if not report:
            await query.message.answer(lang_phrases(lang, 14), parse_mode=HTML)
        count = 0
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

            await query.message.answer(lang_phrases(lang, 12).format(name.strip(), date, subject,
                                                                     topic, tasks, done, right_task, bonus, note))
            count += 1
            # else:
            #     await query.message.answer('В данный момент оценок нет')
            if count > 3:
                break
        await state.finish()
    elif query.data == 'net':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(lang_phrases(lang, 7), callback_data='again'))
        await query.message.answer(lang_phrases(lang, 8), parse_mode=HTML, reply_markup=markup)
        await States.lang.set()


def get_percent(full, value):
    percent = (int(value) * 100) / int(full)
    return '(%.1f ' % percent + '%)'


@dp.callback_query_handler(state=States.delete)
async def delete_step(query: types.CallbackQuery, state: FSMContext):
    print(query)
    if query.data == '/start':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await query.message.answer(lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()
    else:
        data = query.data
        data = data.split('/')
        name = data[0]
        chat_id = data[1]
        delete_from_chat(chat_id=chat_id, name=name)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await query.message.answer('Вы успешно отписались!')
        await query.message.answer(lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()


@dp.message_handler(commands=['delete'])
async def delete(message: types.Message):
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await message.answer(lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()
    list_of_students = select_by_id(message.chat.id)
    inline = types.InlineKeyboardMarkup()
    lang = 1
    for i in list_of_students:
        lang = i[2]
        inline.add(types.InlineKeyboardButton(i[3], callback_data=str(i[3]) + '/' + str(message.chat.id)))
    inline.add(types.InlineKeyboardButton('Назад', callback_data='/start'))
    await bot.send_message(message.chat.id, lang_phrases(lang, 15), reply_markup=inline)
    await States.delete.set()


async def send_message():
    await bot.send_message(877012379, 'send message')
    l = select()
    for j in l:
        time.sleep(1)
        report = await get_grade(j[1])
        bonus = ''
        note = ''
        done = ''
        tasks = ''
        right_task = ''
        for i in report:
            length = len(i)
            time_from = i[1]
            date = time_from[:10]
            topic = i[3]
            subject = i[2]
            if length == 7:
                done = i[4]
                bonus = i[5]
                note = i[6]
            elif length == 9:
                done = i[5]
                tasks = i[6]
                right_task = i[4]
                bonus = i[7]
                note = i[8]
            if bonus is None:
                bonus = ''
            if note is None:
                note = ''
            if date == str(datetime.datetime.today().date()):
                await bot.send_message(j[0], lang_phrases(j[2], 12).format(j[3],
                                                                           date, subject,
                                                                           topic, tasks, done,
                                                                           right_task, bonus, note))


def repeat(coro, loop):
    x = datetime.datetime.today()
    y = x.replace(day=x.day, hour=14, minute=0, second=0, microsecond=0)
    delta_t = y - x
    secs = delta_t.seconds
    print('seconds in repeat ' + str(secs))
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(secs, repeat, coro, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    x = datetime.datetime.today()
    y = x.replace(day=x.day, hour=14, minute=2, second=0, microsecond=0)
    delta_t = y - x
    secs = delta_t.seconds
    print('seconds in main ' + str(secs))
    loop.call_later(secs, repeat, send_message, loop)
    executor.start_polling(dp, loop=loop)
