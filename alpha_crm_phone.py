import json
import requests
from config import email, site, api


def is_phone(p):
    i = 0
    while i < 100:
        i += 0
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
        a = json.loads(customer)
        if 'total' in a:
            x = int(a['total'])
            ids = list()
            for i in range(x):
                ids.append(a['items'][i]['id'])
            return ids