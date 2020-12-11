#!/usr/bin/env python3

from gpiozero import Button
from time import sleep
import subprocess
import os
import signal

key1 = Button(18)
key2 = Button(23)
key3 = Button(24)

while True:
    if key1.is_pressed:
        p = subprocess.Popen('exec fim /home/pi/qrcode.png', shell=True, preexec_fn=os.setsid)
        sleep(15)
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    if key2.is_pressed:
        subprocess.run(['changePassword.py'])
    if key3.is_pressed:
        os.system('clear')
