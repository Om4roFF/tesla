import datetime
import time

from alpha_crm_grade import get_grade
from alpha_crm_lesson import get_lesson_grade
from database import select, select_by_status, update_status, delete_from_lessons
from bot import bot
from lang_list import lang_phrases
import schedule


def send_message():
    l = select()
    print(l)
    for j in l:
        s = select_by_status(j[1])
        print(s)
        try:
            for m in s:
                try:
                    report = get_lesson_grade(m[1], m[0])
                    print(report)
                except Exception as e:
                    bot.send_message(877012379, 'send_msg ' + str(e))
                    time.sleep(20)
                    report = get_grade(j[1])
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
                    bot.send_message(j[0],
                                     lang_phrases(j[2], 12).format(j[3],
                                                                   date, subject,
                                                                   topic, tasks, done,
                                                                   right_task, bonus, note))
                update_status(student_id=j[1], lesson_id=m[1])
        except Exception as e:
            bot.send_message(877012379, str(e))
    delete_from_lessons()


schedule.every().day.at('20:00').do(send_message)

while True:
    schedule.run_pending()
    time.sleep(1)

