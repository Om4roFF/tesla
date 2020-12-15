import re

import requests
import json
from config import email, site, api


def customers(id):
    i = 0
    while i < 100:
        i += 1
        token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                              json={'email': email, 'api_key': api}).text
        TOKEN = token[10:len(token) - 2]
        headers = {'X-ALFACRM-TOKEN': TOKEN}
        customer = requests.post('https://{0}.s20.online/v2api/1/customer/index'.format(site), headers=headers,
                                 json={"id": id}).content
        customer = customer.decode('utf-8')
        a = json.loads(customer.replace("'", '"'))
        if 'items' in a:
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


print(customers(1630))