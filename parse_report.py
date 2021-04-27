import time

import schedule

from alpha_crm_grade import get_grade
from database import select, insert_lessons, create_lessons


def download_report():
    create_lessons()
    l = select()
    for i in l:
        report = get_grade(i[1])
        print(report)
        for j in report:
            insert_lessons(i[1], j.lesson_id, j.date, status=0)


schedule.every().day.at('09:38').do(download_report)

while True:
    schedule.run_pending()
    time.sleep(1)