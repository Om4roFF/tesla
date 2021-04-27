import datetime
import time

import telebot

from alpha_crm_grade import get_grade
from alpha_crm_lesson import get_lesson_grade
from database import select, select_by_status, update_status, delete_from_lessons
from bot import bot
from lang_list import lang_phrases
import schedule


def send_message():
    l = select()
    for j in l:
        s = select_by_status(j[1])

        for m in s:
            try:
                report = get_lesson_grade(m[1], m[0])
                for lesson in report:
                    time_from = lesson.date
                    date = time_from[:10]
                    topic = lesson.topic
                    subject = lesson.subject
                    grade = lesson.grade
                    bonus = lesson.bonus
                    note = lesson.note
                    if bonus is None:
                        bonus = ''
                    if note is None:
                        note = ''
                    bot.send_message(j[0],
                                     lang_phrases(j[2], 12).format(j[3],
                                                                   date, subject, topic, grade, bonus, note))
                update_status(student_id=j[1], lesson_id=m[1])
            except Exception as e:
                print(e)
    delete_from_lessons()


schedule.every().day.at('09:39').do(send_message)

while True:
    schedule.run_pending()
    time.sleep(1)

