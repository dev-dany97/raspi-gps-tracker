#!/usr/local/bin/python3.8
# Filename: send_message.py
#author: d.mohles
import serial
import time
BAUDRATE = 115200
ser = serial.Serial("/dev/ttyS0", BAUDRATE)

W_buff = ["AT\r\n", "AT+CMGF=1\r\n", "AT+CSCA=\"+447797704000\"\r\n", "AT+CMGS=\"0XXXXXXXXXX\"\r\n", "hello world"]
for command in W_buff:
    time.sleep(4)
    print(command)
    ser.write(command.encode())
    #ser.flushInput()
    data=""
    while ser.inWaiting() > 0:

        data += ser.read(ser.inWaiting()).decode("utf-8")
    print(data)
