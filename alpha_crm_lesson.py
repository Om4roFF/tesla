import json
import requests
from config import email, site, api
from database import select


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
        print(TOKEN)
        report = list()
        lessons1 = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), json={'id': lesson_id},
                                 headers=headers).text
        b = json.loads(lessons1)
        print(b)
        if 'items' in b:
            total = b['total']
            items = b['items']
            if total > 20:
                total = 20
            for i in range(total):
                details = items[i]['details']
                for j in details:
                    if j['customer_id'] == student_id:
                        l = list()
                        time_from = items[i]['time_from']
                        time_to = items[i]['time_to']
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
                        grades = grade.split('/')
                        lesson_id = j['lesson_id']
                        l.append(lesson_id)
                        l.append(time_from)
                        l.append(name)
                        l.append(topic)
                        if len(grades) > 1:
                            was = grades[0]
                            done = grades[1]
                            right = grades[2]
                            l.append(was)
                            l.append(done)
                            l.append(right)
                        else:
                            l.append(grade)
                        l.append(bonus)
                        l.append(note)
                        report.append(l)
            return report


print(get_lesson_grade(4141, 1630))

