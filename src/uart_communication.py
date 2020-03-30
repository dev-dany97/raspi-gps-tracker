#!/usr/local/bin/python3.8
# coding=utf-8
# Filename: uart_communication.py
# author: d.mohles
# This lib provides Serial Port functionality

import re
import time
import logging

from serial import Serial, SerialException

from constants import BAUDRATE, COMMON_PORT_NAME, W_TIMEOUT, R_TIMEOUT, ENTER_KEY, bcolors, ERROR_STRING, OK_STRING


# from termcolor import colored


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
        self.last_send_data = ""
        self.read_buffer = ""
        self.ser = Serial(port=COMMON_PORT_NAME, baudrate=BAUDRATE, write_timeout=W_TIMEOUT, timeout=R_TIMEOUT)
        if not self.port_is_open():
            self.open_connection

    def convert_to_ascii_format(self, normal_text):
        """
        Print ascii chars
        :return:
        """
        normal_text = normal_text.replace('\r', '\\r')
        normal_text = normal_text.replace('"', '\"')
        ascii_text = normal_text.replace('\n', '\\n')
        return ascii_text

    @property
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
            logging.error("Port couldn't be open: ", e.message)
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
            logging.error("SEND Status can't be read: ", e.message)
            return False

    def send_data(self, data, check_response=False):
        """
        Send Data on UART interface (default response = 'OK')
        :return: status (True: successfully; False: Failed)
        :rtype: bool
        """
        self.last_send_data = data
        data_buffer = data + ENTER_KEY  # 'data_string' + '\r\n'
        # try until response
        response = False
        while not response:
            try:
                self.read_buffer = ""
                self.ser.reset_input_buffer()  # Flush input buffer, discarding all its contents.
                self.ser.write(data_buffer.encode())
                logging.info("SEND DATA: %s" % self.convert_to_ascii_format(data))
                time.sleep(0.5)  # secure time sleep
                # check response
                if check_response:
                    positive_response = data + '\r' + ENTER_KEY + OK_STRING
                    negative_response = data + '\r' + ENTER_KEY + ERROR_STRING
                    response = self.receive_data()
                    if response == positive_response:
                        logging.info('OK response')
                        response = True
                    elif response == negative_response:
                        self.negative_response_counter += 1
                        if self.negative_response_counter >= self.max_negative_response_counter:
                            return False
                        logging.error('ERROR response')
                        response = True
                    else:
                        response = False
                else:
                    # if no response is expected
                    break
            except Exception as e:
                logging.error('SEND DATA FAILED: ', e.message)
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

    def receive_data(self, equal_value=None):
        """
        Receive data on UART interface
        :return: read_buffer data or True/False if buffer is compared with equal_value
        :rtype: ascii string or bool
        """
        self.read_buffer = ""
        try:
            while self.ser.inWaiting() > 0:
                self.read_buffer += self.ser.read(self.ser.inWaiting()).decode("utf-8")
        except Exception as e:
            logging.error("READ DATA FAILED: ", e.message)
            self.read_buffer = None
        logging.info('RECEIVED DATA: %s' % self.convert_to_ascii_format(self.read_buffer))
        if equal_value:
            expected_pattern = re.compile(r''.join(self.last_send_data + '\r\r\n' + equal_value))
            expected_pattern.match(self.read_buffer)
            if expected_pattern.match(self.read_buffer):
                return True
        return self.read_buffer

    def send_sms(self, msg):
        """

        :return:
        """
        W_buff = ["AT\r\n", "AT+CMGF=1\r\n", "AT+CSCA=\"+447797704000\"\r\n", "AT+CMGS=\"+49XXXXXXXXXX\"\r\n", msg]
        self.ser.write(W_buff[0].encode())
        self.ser.flushInput()
        data = ""
        num = 0

        self.send_data("AT+CMGF=1", check_response=True)
        self.send_data("AT+CSCA=\"+447797704000\"", check_response=True)
        self.send_data("AT+CMGS=\"+49XXXXXXXXXX\"")

        while True:
            while self.ser.inWaiting() > 0:
                data += str(self.ser.read(self.ser.inWaiting()))
            if data != "" and data.count(">") > 0:
                time.sleep(0.5)
                self.ser.write(msg.encode())
                self.ser.write("\x1a\r\n".encode())  # 0x1a : send   0x1b : Cancel send
                break
            data = ""

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
            logging.error("Port couldn't be closed: ", e.message)
            return False
