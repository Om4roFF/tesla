import json
import requests
from config import email, site, api


def get_grade(ID):
    token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                          json={'email': email, 'api_key': api}).text

    TOKEN = token[10:len(token) - 2]
    headers = {'X-ALFACRM-TOKEN': TOKEN}
    report = list()
    lessons1 = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), json={'customer_id': ID},
                             headers=headers).text
    b = json.loads(lessons1)
    print(b)
    total = b['total']
    items = b['items']
    if total > 20:
        total = 20
    for i in range(total):
        details = items[i]['details']
        for j in details:
            if j['customer_id'] == ID:
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