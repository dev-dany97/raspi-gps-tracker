import time
import requests
import math
import random

TOKEN = "YOUR-UBIDOTS-TOKEN"  # TOKEN
API_KEY = "YOUR-UBIDOTS-API-KEY"  # API Key
DEVICE_LABEL = "raspberryPiGPSTracker"  # Device label
VARIABLE_LABEL_1 = "Time"  # Put your first variable label here
VARIABLE_LABEL_2 = "variable2"  # Put your second variable label here
VARIABLE_LABEL_3 = "position"  # Put your second variable label here
LAT=51.013432
LNG=12.101624


def build_payload(variable_1, variable_2, variable_3):
    # Creates two random values for sending data
    value_1 = random.randint(-10, 50)
    value_2 = random.randint(0, 85)

    # Creates payload data
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: {"lat": LAT, "lng": LNG}}
    print(payload)
    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False
    if status == 200:
        print("[INFO] request successfully updated")
    else:
        print("[INFO] request made properly, your device is updated")
    return True


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
