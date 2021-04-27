import json
import requests
from config import email, site, api
from lesson_model import Lesson


def get_id_by_lesson(i_d):
    i = 0
    while i < 100:
        i += 1
        token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                              json={'email': email, 'api_key': api}).text

        TOKEN = token[10:len(token) - 2]
        headers = {'X-ALFACRM-TOKEN': TOKEN}
        lessons = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), headers=headers, json={'customer_id': i_d}).text
        a = json.loads(lessons)
        if 'total' in a:
            total = a['total']
            if total > 0:
                return i_d
            return 0


def get_lesson_grade(lesson_id, student_id):
    i = 0
    while i < 100:
        i += 1
        token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                              json={'email': email, 'api_key': api}).text

        TOKEN = token[10:len(token) - 2]
        headers = {'X-ALFACRM-TOKEN': TOKEN}
        report = list()
        lessons1 = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), json={'id': lesson_id},
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
                    if j['customer_id'] == student_id:
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
