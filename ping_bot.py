#!/usr/bin/python3

import requests
import os
import subprocess
import time
from datetime import datetime

server_name = 'SERVER' # This server name
ip = 'xx.xx.xx.xx' # checking IP
apiToken = '' # Telegram Tocken
chatID = '' # Telegram chat

file = open('/opt/ping_bot/{}.log'.format(datetime.now().strftime("ping_%m-%d-%y")),'a')
file.close()

def send_to_telegram(message):

    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

def check_time(t):
    maximum = t.split('/')[2]
    if float(maximum) > 300:
        return 1
    else:
        return 0

def ping(host):
    command = ['ping', '-c', '4', host]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    text = str(out)

    if text.count('time=') > 0:
        arr = text.split('\\n')
        result = arr[-2][arr[-2].find(' = ')+3:arr[-2].find(' ms')]
        error = check_time(result)
    else:
        result = 'No Response'
        error = 1

    return error, result

for i in range(30,0,-29):
    ping_rezult = ping(ip)

    if ping_rezult[0] == 1:
        send_to_telegram('PING ERROR\n' + server_name + ' to ' + ip + '\nmin/avg/max/mdev = ' + ping_rezult[1])

    os.system('echo "{} ERROR: {}; IP: {}; min/avg/max/mdev = {}" >> /opt/ping_bot/{}.log'.format(datetime.now().strftime("%m-%d-%y %X"), str(ping_rezult[0]), str(ip), str(ping_rezult[1]), datetime.now().strftime("ping_%m-%d-%y")))

    time.sleep(i)
