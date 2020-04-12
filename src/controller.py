#!/usr/local/bin/python3.8
# Filename: gps_module.py
# author: d.mohles
# Script for controlling GSM/GPRS/GNSS HAT
import logging
import sys
import threading
from datetime import datetime, timedelta
from time import sleep, strftime

from serial import SerialException

from constants import INTRO_HEADER, GPS_COMMANDS
from gps_module import GPS
from gsm_pwrkey import start_board
from message import Message
from uart_communication import UART
from ubi_api import UbiApi


def main():
    """
    Main function (entry point)
    :return:
    """
    last_lat = 0
    last_lng = 0
    last_timestamp = datetime.now()
    last_coordinate_timestamp = datetime.now()

    format = "%(asctime)s[%(levelname)s]: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    print(INTRO_HEADER)
    com_handler = None
    # declare message
    msg_block = Message()
    # open Serial Port communication
    connecetion_established = False
    connection_timeout = 0
    board_started = False
    while not connecetion_established:
        try:
            com_handler = UART()
            connecetion_established = True
        except SerialException as e:
            connection_timeout += 1
            sys.stdout.write(
                '\r{0}[INFO]: wait for connection...{1}'.format(strftime("%H:%M:%S"), '.' * connection_timeout))
            logging.debug("\nSerial Port Problem: %s" % e.strerror)
            sleep(5)
        except Exception as e:
            connecetion_established = False
            logging.error("\nConnection Problem: %s" % e)
            sleep(5)
    # disable disable gps module
    com_handler.send_data(GPS_COMMANDS["GPS_POWER_OFF"])
    com_handler.check_response_in_data_flow(GPS_COMMANDS["GPS_POWER_OFF"])

    while not com_handler.send_data("AT", check_response=True):
        if not board_started:
            logging.info("start board...")
            start_board()
            board_started = True
            logging.info("board started!")
        logging.info("wait for answer...")
    logging.info("connection established!")

    # init handlers
    gps_handler = GPS(com_handler, msg_block)

    upload_handler = UbiApi(com_handler, msg_block)

    # run GPS module
    while True:
        x = threading.Thread(target=gps_handler.start)  # run gps handler in extra thread
        x.start()
        logging.debug("GPS Thread: I'm running")
        counter = 1
        while True:
            # wait if data is received
            if msg_block.lat and msg_block.lng:
                # Check if data was updated:
                if last_lat != msg_block.lat or last_lng != msg_block.lng:
                    if datetime.now() >= last_coordinate_timestamp + timedelta(seconds=5):
                        # set new values to old values
                        last_lat = msg_block.lat
                        last_lng = msg_block.lng
                        logging.info("LAT or LNG changed!")
                        logging.info("GPS Latitude: " + str(msg_block.lat))
                        logging.info("GPS Longitude: " + str(msg_block.lng))
                        x2 = threading.Thread(target=gps_handler.stop)
                        x2.start()  # send stop signal
                        x2.join()
                        x.join()
                        upload_handler.upload_data()
                        last_coordinate_timestamp = datetime.now()
                        break

                if datetime.now() >= last_timestamp + timedelta(days=1):
                    # send every day a status message
                    last_timestamp = datetime.now()
                    # send message
                    com_handler.send_sms("Hi I'm online!\nMy last location:\nlat=" + str(msg_block.lat) + "\nlong=" +
                                         str(msg_block.lat))
            sleep(0.5)

    ##### FOR TESTING #####

    # gps_handler.run()  # endless loop, if no stop command send!
    # start thread upload handler
    # msg_block.lat = 51.013432
    # msg_block.lng = 12.101624
    # msg_block.timestamp = 27032020111260

    # every 30sec upload data
    # while True:
    #    upload_handler.upload_data()
    #    sleep(30)
    #    #msg_block.lat += 0.1
    #    #msg_block.lng += 0.1
    #    #msg_block.timestamp += 1


if __name__ == '__main__':
    exception_counter = 0
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logging.fatal("Error: ", e)
        exception_counter += 1
        if exception_counter > 3:
            logging.debug("exception counter:", exception_counter)
            sys.exit(1)
