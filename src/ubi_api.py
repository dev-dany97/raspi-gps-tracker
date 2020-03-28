#!/usr/local/bin/python3.8
# Filename: ubi_api.py
# author: d.mohles
# This lib provides UBI Dots API interface functionality

import time
import requests
import random


class UbiApi:

    UBI_DOTS_URL = "http://industrial.api.ubidots.com"
    TOKEN = "YOUR-UBIDOTS-TOKEN"  # TOKEN
    API_KEY = "YOUR-UBIDOTS-API-KEY"  # API Key
    DEVICE_LABEL = "raspberryPiGPSTracker"  # Device label
    Time_LABEL = "timestamp"  # Put your first variable label here
    VARIABLE_LABEL = "variable"  # Put your second variable label here
    Position_LABEL = "position"  # Put your second variable label here
    #LAT = 51.013432
    #LNG = 12.101624

    def __init__(self, msg_block):
        """
        Init UBI API
        """
        self._msg_block = msg_block

    def upload_data(self):
        """
        Upload data to UBI website
        :return:
        """
        payload = self._build_payload()
        print("[INFO] Attemping to send data")
        self._post_request(payload)
        print("[INFO] finished")

    def _build_payload(self):
        """

        :return:
        """
        # Creates a random values for sending data
        value_2 = random.randint(0, 85)

        # Creates payload data
        payload = {self.Time_LABEL: self._msg_block.timestamp,
                   self.VARIABLE_LABEL: value_2,
                   self.Position_LABEL: {"lat": self._msg_block.lat, "lng": self._msg_block.lng}}
        return payload

    def _post_request(self, payload):
        """

        :param payload:
        :return:
        """
        # Creates the headers for the HTTP requests
        url = "{}/api/v1.6/devices/{}".format(self.UBI_DOTS_URL, self.DEVICE_LABEL)
        headers = {"X-Auth-Token": self.TOKEN, "Content-Type": "application/json"}

        # Makes the HTTP requests
        status = 400
        attempts = 0
        while status >= 400 and attempts <= 5:
            print("send message: ", payload)
            req = requests.post(url=url, headers=headers, json=payload)
            status = req.status_code
            attempts += 1
            time.sleep(1)

        # Processes results
        # more response codes: https://ubidots.com/docs/hw/#retrieve-the-last-value-for-control
        if status >= 400:
            print("[ERROR] Could not send data after 5 attempts, please check \
                your token credentials and internet connection")
            return False
        if status == 200:
            print("[INFO] request successfully updated")
        else:
            print("[INFO] request made properly, your device is updated")
        return True


'''
def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
'''
