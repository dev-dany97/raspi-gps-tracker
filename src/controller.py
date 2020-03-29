#!/usr/local/bin/python3.8
# Filename: gps_module.py
# author: d.mohles
# Script for controlling GSM/GPRS/GNSS HAT

from serial import SerialException
import sys
from time import sleep

from constants import INTRO_HEADER
from uart_communication import UART
from gps_module import GPS
from ubi_api import UbiApi
from message import Message


def main():
    """
    Main function (entry point)
    :return:
    """
    print(INTRO_HEADER)
    com_handler = None
    # declare message
    msg_block = Message()
    # open Serial Port communication
    connecetion_established = False
    while not connecetion_established:
        try:
            com_handler = UART()
            connecetion_established = True
        except SerialException as e:
            print("[INFO] wait for connection...")
            print("[DEBUG] wait for connection... Message:", e)
            sleep(5)
        except Exception as e:
            print("[ERROR] Connection Problem: ", e)
            sleep(5)
    print("[INFO] connection established!")
    com_handler.send_data("AT", check_response=True)
    
    # start thread gps handler
    ## gps_handler = GPS(com_handler, msg_block)
    # run GPS module
    ## gps_handler.run()  # endless loop, if no stop command send!
    # start thread upload handler
    msg_block.lat = 51.013432
    msg_block.lng = 12.101624
    msg_block.timestamp = 27032020111260
    upload_handler = UbiApi(com_handler, msg_block)

    # every 30sec upload data
    while True:
        upload_handler.upload_data()
        sleep(30)
        msg_block.lat += 0.1
        msg_block.lng += 0.1
        msg_block.timestamp += 1


if __name__ == '__main__':
    sys.exit(main())