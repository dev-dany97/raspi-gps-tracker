#!/usr/local/bin/python3.8
# Filename: gps.py
# author: d.mohles

import datetime
import serial
import time
import re
from .constants import CGNSINF_Struct

BAUDRATE = 115200
ser = serial.Serial("/dev/ttyS0", BAUDRATE)


W_buff = ["AT+CGNSPWR=1\r\n", "AT+CGNSSEQ=\"RMC\"\r\n", "AT+CGNSINF\r\n", "AT+CGNSURC=40\r\n", "AT+CGNSTST=0\r\n"]# "AT+CGNSINF\r\n"] #"AT+CGNSTST=1\r\n"]
ser.write(str.encode(W_buff[0]))
ser.flushInput()
data = ""
num = 0


def convert_utc_time(timestamp):
    """

    :param timestamp:
    :return:
    """
    return datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')

try:
    while True:
        while ser.inWaiting() > 0:
            data += ser.read(ser.inWaiting()).decode("utf-8")
            print(data)
            gps_matches = re.findall("(CGNSINF: (1|0),(1|0),(.{18}),([0-9.]{0,10}),([0-9.]{0,11}),([0-9.]{0,8}),([0-9.]{0,6}),"
                             "([0-9.]{0,6}),(0|1|2),([\w\d.]*),([0-9.]{0,4}),([0-9.]{0,4}),([0-9.]{0,4}),([\w\d.]*),"
                             "([0-9.]{0,2}),([0-9.]{0,2}),([0-9.]{0,2}),([\w\d.]*),([0-9]{0,2}),([0-9.]{0,6}),"
                             "([0-9.]{0,6}))", data)
            for gps_data in gps_matches:
                date = datetime.datetime.strptime('20200314212323.000', '%Y%m%d%H%M%S.%f')
                print("---------------------------------------------")
                print("UTC Date Time = " + str(convert_utc_time(gps_data[CGNSINF_Struct.utc_date_time])))
                print("Latitude is = " + gps_data[CGNSINF_Struct.latitude])
                print("Longitude is = " + gps_data[CGNSINF_Struct.longitude])
                print("GPS Satellites in View = " + gps_data[CGNSINF_Struct.gps_satellites_in_view])
                print("GNSS Satellites Used = " + gps_data[CGNSINF_Struct.gnss_satellites_used])
                print("GLONASS Satellites in View = " + gps_data[CGNSINF_Struct.glonass_satellites_in_view])
                print("Speed = " + gps_data[CGNSINF_Struct.speed_over_ground])
                print("Course = " + gps_data[CGNSINF_Struct.course_over_ground])
            #print(data)
        if data != "" and num <= 3:
            time.sleep(0.5)
            ser.write(str.encode(W_buff[num + 1]))
            num = num + 1
        if num == 4:
            time.sleep(0.5)
            ser.write(str.encode(W_buff[4]))
            num = num + 1
        data = ""
except KeyboardInterrupt:
    if ser is not None:
        ser.close()
