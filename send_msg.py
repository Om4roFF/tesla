import datetime
import time

from alpha_crm_grade import get_grade
from database import select
from bot import bot
from lang_list import lang_phrases
import schedule


def send_message(message=None):
    try:
        l = select()
        for j in l:
            time.sleep(1)
            try:
                report = get_grade(j[1])
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
                if date == str(datetime.datetime.today().date()):
                    bot.send_message(j[0], lang_phrases(j[2], 12).format(j[3],
                                                                         date, subject,
                                                                         topic, tasks, done,
                                                                         right_task, bonus, note))
    except Exception as e:
        bot.send_message(877012379, str(e))


schedule.every().day.at('14:00').do(send_message)

while True:
    schedule.run_pending()
    time.sleep(1)
