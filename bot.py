import datetime
from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from AlphaCRM import customers, get_name, get_grade, is_phone
from database import create_table, insert, select, is_user
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
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await message.answer(lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()
    else:
        id = is_phone(message.text)
        # print(id)
        data = await state.get_data()
        lang = data.get('lang')
        await state.update_data(id=id)
        if id:
            await message.answer(lang_phrases(lang, 0), parse_mode=HTML)
            await States.id.set()
        else:
            await message.answer(lang_phrases(lang, 2), parse_mode=HTML)
            await States.phone.set()


@dp.message_handler(state=States.id)
async def id_step(message: types.Message, state: FSMContext):
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Рус ' + "🇷🇺", callback_data='Рус'))
        markup.add(types.InlineKeyboardButton(text='Қаз ' + "🇰🇿", callback_data='Қаз'))
        await message.answer(lang_phrases(1, 10), reply_markup=markup, parse_mode=HTML)
        await States.lang.set()
    else:
        id = message.text
        data = await state.get_data()
        i_d = data.get('id')
        lang = data.get('lang')
        if int(id) == int(i_d):
            customer = customers(id)
            name = get_name(customer)
            await state.update_data(name=name)
            await state.update_data(id=id)
            inline_markup = types.InlineKeyboardMarkup()
            inline_markup.add(types.InlineKeyboardButton(lang_phrases(lang, 4), callback_data='da'))
            inline_markup.add(types.InlineKeyboardButton(lang_phrases(lang, 5), callback_data='net'))
            create_table()
            insert(message.chat.id, id, lang, name.strip())
            await message.answer(lang_phrases(lang, 3).format(str(name)), reply_markup=inline_markup, parse_mode=HTML)
            await States.grade.set()
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(lang_phrases(lang, 7), callback_data='again'))
            await message.answer(lang_phrases(lang, 6), parse_mode=HTML, reply_markup=markup)
            await States.lang.set()


@dp.callback_query_handler(state=States.grade)
async def grade_step(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    name = data.get('name')
    if query.data == 'da':
        if not is_user(query.message.chat.id):
            await query.message.answer(lang_phrases(lang, 13), parse_mode=HTML)
        msg = await query.message.answer(lang_phrases(lang, 9), parse_mode=HTML)
        data = await state.get_data()
        id = data.get('id')
        report = get_grade(int(id))
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
                bonus = i[7]
                note = i[8]
            if bonus is None:
                bonus = ''
            if note is None:
                note = ''

            await query.message.answer(lang_phrases(lang, 12).format(name, date, subject,
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


async def send_message():
    l = select()
    for j in l:
        report = get_grade(j[1])
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
                bonus = i[7]
                note = i[8]
            if bonus is None:
                bonus = ''
            if note is None:
                note = ''

            await bot.send_message(j[0], lang_phrases(j[2], 12).format(j[3], date, subject,
                                                                       topic, tasks, done, right_task, bonus, note))
            break


def repeat(coro, loop):
    x = datetime.datetime.today()
    y = x.replace(day=x.day, hour=0, minute=2, second=0, microsecond=0)
    delta_t = y - x
    secs = delta_t.seconds
    print('secs in repeat')
    print(secs)
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(secs, repeat, coro, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    x = datetime.datetime.today()
    y = x.replace(day=x.day, hour=1, minute=27, second=0, microsecond=0)
    delta_t = y - x
    secs = delta_t.seconds
    print(secs)
    loop.call_later(secs, repeat, send_message, loop)
    executor.start_polling(dp, loop=loop)
