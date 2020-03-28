#!/usr/local/bin/python3.8
# Filename: uart_communication.py
# author: d.mohles
# This lib provides Serial Port functionality

from serial import Serial, SerialException
import time
import re
#from termcolor import colored

from constants import BAUDRATE, COMMON_PORT_NAME, W_TIMEOUT, R_TIMEOUT, ENTER_KEY, bcolors, ERROR_STRING, OK_STRING


class UART(object):
    """
    Provide UART Communication functions
    """
    max_negative_response_counter = 20
    negative_response_counter = 0

    def __init__(self):
        """
        Init UART
        """
        self.read_buffer = ""
        self.ser = Serial(port=COMMON_PORT_NAME, baudrate=BAUDRATE, write_timeout=W_TIMEOUT, timeout=R_TIMEOUT)
        if not self.port_is_open():
            self.open_connection()

    def convert_to_ascii_format(self, normal_text):
        """
        Print ascii chars
        :return:
        """
        normal_text = normal_text.replace('\r', '\\r')
        normal_text = normal_text.replace('"', '\"')
        ascii_text = normal_text.replace('\n', '\\n')
        return ascii_text

    def open_connection(self):
        """
        Opens SerialPort connection
        :return: True:= successfully open, False:= Can't be open
        :rtype: bool
        """
        try:
            if self.port_is_open():
                return True
            self.ser.open()
        except SerialException as e:
            print("Port couldn't be open: ", e)
            return False
        return True

    def port_is_open(self):
        """
        Get the state of the serial port, whether it’s open.
        :return: True:= Port open, False:= Port closed
        :rtype: bool
        """
        try:
            return self.ser.is_open
        except Exception as e:
            print("SEND Status can't be read: ", e)
            return False

    def send_data(self, data, check_response=False):
        """
        Send Data on UART interface (default response = 'OK')
        :return: status (True: successfully; False: Failed)
        :rtype: bool
        """
        data_buffer = data + ENTER_KEY  # 'data_string' + '\r\n'
        # try until response
        response = False
        while not response:
            try:
                self.read_buffer = ""
                self.ser.reset_input_buffer()  # Flush input buffer, discarding all its contents.
                self.ser.write(data_buffer.encode())
                print(f"{bcolors.SENDER}[INFO] SEND DATA: {self.convert_to_ascii_format(data)}{bcolors.ENDC}")
                time.sleep(0.5)  # secure time sleep
                # check response
                if check_response:
                    positive_response = data + '\r' + ENTER_KEY + OK_STRING
                    negative_response = data + '\r' + ENTER_KEY + ERROR_STRING
                    response = self.receive_data()
                    if response == positive_response:
                        print(
                            f"{bcolors.RECEIVER}[INFO] OK response{bcolors.ENDC}")
                        response = True
                    elif response == negative_response:
                        self.negative_response_counter += 1
                        if self.negative_response_counter >= self.max_negative_response_counter:
                            return False
                        print(
                            f"{bcolors.RECEIVER}[INFO] ERROR response{bcolors.ENDC}")
                        response = True
                    else:
                        response = False
                else:
                    # if no response is expected
                    break
            except Exception as e:
                print(f"{bcolors.ERROR}[ERROR] SEND DATA FAILED: {e}{bcolors.ENDC}")
                return False

    def check_response_in_data_flow(self, data):
        positive_response_regex = r''.format(data + '\r' + ENTER_KEY + OK_STRING)
        negative_response_regex = r''.format(data + '\r' + ENTER_KEY + ERROR_STRING)
        answer = self.receive_data()
        positive_pattern = re.compile(positive_response_regex)
        negative_pattern = re.compile(negative_response_regex)
        if positive_pattern.search(answer) or negative_pattern.search(answer):
            # if answer matched with expected response
            return True
        else:
            # answer didn't matched
            return False

    def receive_data(self):
        """
        Receive data on UART interface
        :return: read_buffer
        :rtype: ascii string
        """
        self.read_buffer = ""
        try:
            while self.ser.inWaiting() > 0:
                self.read_buffer += self.ser.read(self.ser.inWaiting()).decode("utf-8")
        except Exception as e:
            print("[ERROR] READ DATA FAILED: ", e)
            print(f"{bcolors.ERROR}[ERROR] READ DATA FAILED: {e}{bcolors.ENDC}")
            self.read_buffer = None
        print(f"{bcolors.RECEIVER}[INFO] RECEIVED DATA: {self.convert_to_ascii_format(self.read_buffer)}{bcolors.ENDC}")
        return self.read_buffer

    def close_connection(self):
        """
        Close SerialPort connection immediately
        :return: True:= Port successfully closed, False:= Port can't be closed
        :rtype: bool
        """
        try:
            self.ser.close()
            return True
        except Exception as e:
            print("Port couldn't be closed: ", e)
            return False
