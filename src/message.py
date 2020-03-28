#!/usr/local/bin/python3.8
# Filename: gps_module.py
# author: d.mohles
# This lib defines the message bus


class Message:
    """
    Defines data package
    """

    def __init__(self):
        self._timestamp = None
        self._lat = None
        self._lng = None

    # using property decorator
    # time getter function
    @property
    def timestamp(self):
        print("getter method called")
        return self._timestamp

    # time setter function
    @timestamp.setter
    def timestamp(self, time_stamp):
        if type(time_stamp) != int:
            raise ValueError("[ERROR] time format type is != string!")
        print("setter method called")
        self._timestamp = time_stamp

    # latitude getter function
    @property
    def lat(self):
        print("getter method called")
        return self._lat

    # latitude setter function
    @lat.setter
    def lat(self, latitude):
        if type(latitude) != float:
            raise ValueError("[ERROR] latitude format type should be float or string!")
        print("setter method called")
        self._lat = latitude

    # longitude getter function
    @property
    def lng(self):
        print("getter method called")
        return self._lng

    # longitude setter function
    @lng.setter
    def lng(self, longitude):
        if type(longitude) != float:
            raise ValueError("[ERROR] longitude format type should be float or string!")
        print("setter method called")
        self._lng = longitude

    def getting_msg(self):
        return {'lat': self._lat, 'lng': self._lng, 'timestamp': str(self._timestamp)}
