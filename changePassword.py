#!/usr/bin/env python3

import random
import string
import re
import pyqrcode as pqr
import subprocess

def get_random_pw():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for i in range(12))
    return password

def get_hostapd_text():
    file = open('/etc/hostapd/hostapd.conf', 'r')
    text = file.read()
    file.close()
    return text

def get_wpa():
    text = get_hostapd_text()
    matches = re.findall("wpa=.", text)
    return matches[0].replace('wpa=', 'WPA')

def get_ssid():
    text = get_hostapd_text()
    matches = re.findall("ssid=.*", text)
    return matches[0].replace('ssid=', '')

def create_qr_code(ssid, security, password):
    qr = pqr.create('WIFI:S:{ssid};T:{security};P:{password};;'.format(
        ssid=ssid,
        security=security,
        password=password
    ))
    qr.png('qrcode.png', scale=9)

def change_password(password):
    subprocess.run(
        [
            'sed',
            '-i',
            's/wpa_passphrase=.*/wpa_passphrase={password}/g'.format(
                password=password
            ),
            '/etc/hostapd/hostapd.conf'
        ]
    )
    subprocess.run(['systemctl', 'restart', 'hostapd.service'])

if __name__ == "__main__":
    ssid = get_ssid()
    wpa = get_wpa()
    pw = get_random_pw()
    print('SSID:', ssid,  wpa, 'PW:', pw)
    create_qr_code(ssid, wpa, pw)
    change_password(pw)
