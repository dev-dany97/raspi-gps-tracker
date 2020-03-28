#!/usr/local/bin/python3.8
# Filename: send_message.py
#author: d.mohles
from operator import gt, lt

import serial
import time
from decimal import *
from subprocess import call
BAUDRATE = 115200
ENTER_KEY = '\r\n'

def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i


# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=BAUDRATE, timeout=1)
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

port.write('AT' + ENTER_KEY)
rcv = port.read(100)
print(rcv)
time.sleep(.1)

port.write('AT+CGNSPWR=1' + ENTER_KEY)  # to power the GPS
rcv = port.read(100)
print(rcv)
time.sleep(.1)

port.write('AT+CGNSIPR=115200' + ENTER_KEY)  # Set the baud rate of GPS
rcv = port.read(100)
print(rcv)
time.sleep(.1)

port.write('AT+CGNSTST=1' + ENTER_KEY)  # Send data received to UART
rcv = port.read(100)
print(rcv)
time.sleep(.1)

port.write('AT+CGNSINF' + ENTER_KEY)  # Print the GPS information
rcv = port.read(200)
print(rcv)
time.sleep(.1)
ck = 1
while ck == 1:
    fd = port.read(200)  # Read the GPS data from UART
    # print fd
    time.sleep(.5)
    if '$GNRMC' in fd:  # To Extract Lattitude and
        ps = fd.find('$GNRMC')  # Longitude
        dif = len(fd) - ps
        print(dif)
        print(gt)
        if dif:
            data = fd[ps:(ps + 50)]
            print(data)
            ds = data.find('A')  # Check GPS is valid
            print(ds)
            if ds and ds:
                p = list(find(data, ","))
                lat = data[(p[2] + 1):p[3]]
                lon = data[(p[4] + 1):p[5]]

                # GPS data calculation

                s1 = lat[2:len(lat)]
                s1 = Decimal(s1)
                s1 = s1 / 60
                s11 = int(lat[0:2])
                s1 = s11 + s1

                s2 = lon[3:len(lon)]
                s2 = Decimal(s2)
                s2 = s2 / 60
                s22 = int(lon[0:3])
                s2 = s22 + s2

                print(s1)
                print(s2)
