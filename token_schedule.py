import time

import requests
import schedule
from config import email, site, api
import threading

headers1 = ''


def async_function():
    global headers1
    token = requests.post('https://{0}.s20.online/v2api/auth/login'.format(site),
                          json={'email': email, 'api_key': api}).text

    TOKEN = token[10:len(token) - 2]
    headers1 = {'X-ALFACRM-TOKEN': TOKEN}
    print(headers1)


threading.Timer(1800, async_function).start() # Перезапуск через 30 минут
async_function()
