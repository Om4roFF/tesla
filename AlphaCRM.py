import datetime
import json
import re
import time

import requests
from config import email, site, api


def branches():
    token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                          json={'email': email, 'api_key': api}).text

    TOKEN = token[10:len(token) - 2]
    headers = {'X-ALFACRM-TOKEN': TOKEN}
    branch = requests.post('https://{0}.s20.online/v2api/branch/index'.format(site), headers=headers).content
    branch_str = branch.decode('utf-8')
    # branch_str = branch_str.split('{')
    a = json.loads(branch_str.replace("'", '"'))
    items = a['items']
    items = str(items)
    # items = items.split(',')


def customers(id):
    token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                          json={'email': email, 'api_key': api}).text

    TOKEN = token[10:len(token) - 2]
    headers = {'X-ALFACRM-TOKEN': TOKEN}
    customer = requests.post('https://{0}.s20.online/v2api/1/customer/index'.format(site), headers=headers,
                             json={"id": id}).content
    customer = customer.decode('utf-8')
    a = json.loads(customer.replace("'", '"'))
    all_customers = a['items']
    all_customers = str(all_customers)
    all_customers = all_customers.split('}')
    l = list()
    for i in all_customers:
        b = str(i + '}')
        b = b[1:len(b)]
        l.append(b)
    for i in l:
        user = i.split(',')
        i_d = re.findall("\d", user[0])
        st = ''
        for j in i_d:
            st += j
        if st != '':
            if int(st) == int(id):
                return i


def get_name(text):
    customer_list = text.split(',')
    s = customer_list[3]
    s = s.split(':')
    name = s[1]
    name = name.replace("'", " ")
    return name


def get_grade(ID):
    token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                          json={'email': email, 'api_key': api}).text

    TOKEN = token[10:len(token) - 2]
    headers = {'X-ALFACRM-TOKEN': TOKEN}
    report = list()
    lessons = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), headers=headers).text
    a = json.loads(lessons)
    total = a['total']
    count = int(total) / 20 + 1
    for x in range(int(count)):
        lessons1 = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), json={'page': x},
                                 headers=headers).text
        b = json.loads(lessons1)
        items = b['items']
        for i in items:
            details = i['details']
            for j in details:
                if j['customer_id'] == ID:
                    l = list()
                    time_from = i['time_from']
                    time_to = i['time_to']
                    subject_id = i['subject_id']
                    bonus = j['bonus']
                    topic = i['topic']
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


def is_phone(p):
    token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                          json={'email': email, 'api_key': api}).text

    TOKEN = token[10:len(token) - 2]
    headers = {'X-ALFACRM-TOKEN': TOKEN}
    phone = ''
    if len(p) == 12:
        phone = p[0] + p[1] + '(' + p[2] + p[3] + p[4] + ')' + p[5] + p[6] + p[7] + '-' + p[8] + p[9] + '-' + p[10] + p[11]
    elif len(p) == 11:
        p = p[1:]
        phone = '+' + p[0] + '(' + '7' + p[1] + p[2] + ')' + p[3] + p[4] + p[5] + '-' + p[6] + p[7] + '-' + p[8] + p[9]
    else:
        return None
    customer = requests.post('https://{0}.s20.online/v2api/1/customer/index'.format(site), headers=headers,
                             json={'phone': phone}).text
    a = json.loads(customer.replace("'", '"'))

    items = a['items']
    for i in items:
        return i['id']
    return None


def get_id_by_lesson(i_d):
    token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                          json={'email': email, 'api_key': api}).text

    TOKEN = token[10:len(token) - 2]
    headers = {'X-ALFACRM-TOKEN': TOKEN}
    lessons = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), headers=headers).text
    print(lessons)
    a = json.loads(lessons)
    print(a)
    total = a['total']
    count = int(total) / 20 + 1
    for x in range(int(count)):
        lessons1 = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), json={'page': x},
                                 headers=headers).text
        b = json.loads(lessons1)
        time.sleep(1)
        items = b['items']
        for i in items:
            details = i['details']
            for j in details:
                if i_d == j['customer_id']:
                    return i_d
    return 0


# k = customers(3530)
# print(k)
# name = get_name(k)
# print(name)
# s = get_id_by_lesson(3530)
# print(s)
# id = is_phone('87788881311')
# print(id)
#
# grade = get_grade(3265)
# print(grade)
# +7(707)931-66-28
# token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
#                       json={'email': email, 'api_key': api}).text
#
# TOKEN = token[10:len(token) - 2]
# headers = {'X-ALFACRM-TOKEN': TOKEN}
# for x in range(int(4)):
#
#     lessons1 = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), json={'page': x},
#                              headers=headers).text
#     print(lessons1)
#     b = json.loads(lessons1)
#     items = b['items']
#     print(items)


# get_grade(3530)

