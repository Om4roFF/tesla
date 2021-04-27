import json
import requests
from config import email, site, api
from lesson_model import Lesson


def get_grade(ID):
    i = 0
    while i < 100:
        i += 1
        token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                              json={'email': email, 'api_key': api}).text

        TOKEN = token[10:len(token) - 2]
        headers = {'X-ALFACRM-TOKEN': TOKEN}
        report = list()
        lessons1 = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), json={'customer_id': ID},
                                 headers=headers).text
        b = json.loads(lessons1)
        if 'items' in b:
            total = b['total']
            items = b['items']
            if total > 20:
                total = 20
            for i in range(total):
                details = items[i]['details']
                for j in details:
                    if j['customer_id'] == ID:
                        time_from = items[i]['time_from']
                        subject_id = items[i]['subject_id']
                        bonus = j['bonus']
                        topic = items[i]['topic']
                        note = j['note']
                        subjects = requests.post('https://{0}.s20.online/v2api/1/subject/index'.format(site),
                                                 headers=headers).text
                        subjects = json.loads(subjects.replace("'", '"'))
                        subjects = subjects['items']
                        name = ''
                        for k in subjects:
                            if k['id'] == int(subject_id):
                                name = k['name']
                        grade = j['grade']
                        lesson_id = j['lesson_id']
                        lesson = Lesson(lesson_id, time_from, name, topic, grade, bonus, note)
                        report.append(lesson)
            return report

