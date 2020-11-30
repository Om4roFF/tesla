import json
import requests
from config import email, site, api


def get_id_by_lesson(i_d):
    token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                          json={'email': email, 'api_key': api}).text

    TOKEN = token[10:len(token) - 2]
    headers = {'X-ALFACRM-TOKEN': TOKEN}
    lessons = requests.post('https://{0}.s20.online/v2api/1/lesson/index'.format(site), headers=headers, json={'customer_id': i_d}).text
    a = json.loads(lessons)
    total = a['total']
    if total > 0:
        return i_d
    return 0
