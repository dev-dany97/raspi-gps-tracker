#!/usr/local/bin/python3.8
# Filename: gsm_pwrkey.py
# author: d.mohles
# start gsm board

import time

import RPi.GPIO as GPIO


def start_board():
	"""	Start board
	"""
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)
	while True:
		GPIO.output(7, GPIO.LOW)
		time.sleep(4)
		GPIO.output(7, GPIO.HIGH)
		break
	GPIO.cleanup()
