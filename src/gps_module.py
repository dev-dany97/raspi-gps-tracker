#!/usr/local/bin/python3.8
# Filename: gps_module.py
# author: d.mohles
# This lib provides GNSS functionality for GNSS module

import datetime
import re
import time
import logging
from datetime import datetime

from dateutil import tz

from constants import CGNSINF_Struct, GPS_COMMANDS, bcolors, GNGGA, GNRMC, GPS_STATUS

gnss_data_struct_pattern = r"(CGNSINF: (1|0),(1|0),(.{18}),([0-9.]{0,10}),([0-9.]{0,11}),([0-9.]{0,8}),([0-9.]{0,6})," \
                           r"([0-9.]{0,6}),(0|1|2),([\w\d.]*),([0-9.]{0,4}),([0-9.]{0,4}),([0-9.]{0,4}),([\w\d.]*)," \
                           r"([0-9.]{0,2}),([0-9.]{0,2}),([0-9.]{0,2}),([\w\d.]*),([0-9]{0,2}),([0-9.]{0,6})," \
                           r"([0-9.]{0,6})) "


def convert_utc_time(timestamp):
    """

    :param timestamp:
    :return: returns a datetime string
    :rtype: string
    """
    return str(datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f'))


def convert_utc_date_time(utc_time, date):
    """
    Convert UTC datetime string to local datetime

    :param utc_time: gps utc time
    :type utc_time: string
    :param date: gps utc date
    :type date: string
    :return: timestamp e.g. 2020-03-23 22:01:03+01:00
    :rtype: datetime format
    """
    # Concatenate time and date
    time_stamp = '20{0}-{1}-{2} {3}:{4}:{5}'.format(
        date[4:6], date[2:4], date[0:2], utc_time[0:2], utc_time[2:4], utc_time[4:6])

    # METHOD 1: Hardcode zones:
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Berlin')

    utc = datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = utc.astimezone(to_zone)
    return central


def convert_nmea_to_dec(coord):
    """
    convert gps latitude and longitude of NMEA format data to decimal
    Format: DDDMM.MMMMM => DD deg MM.MMMMM min

    :param coord: gps coordinates DDDMM.MMMMM or DDMM.MMMMM
    :type coord: string
    :return: normal gps coordinate in decimal degrees (latitude longitude MM)
    :rtype: float or None(if coordinate conversion fails)
    """
    try:
        x = coord.split(".")
        head = x[0]
        tail = x[1]
        deg = head[0:-2]
        min = head[-2:]
        # LatDec = DD + SS/60
        coord_deg = int(deg) + float(coord[-9:]) / 60
        logging.info("coordinate: " + deg + " deg " + min + "." + tail + " min")
    except Exception as e:
        logging.error("can't convert coordinates because of: %s" % e.args)
        return None
    return coord_deg


class GPS:
    """
    Provide GNSS module functionality
    """
    gps_module_status = GPS_STATUS['OFF']
    stop_command = True

    def __init__(self, com_handler, msg_block):
        """
        Init GNSS module
        """
        self.com_handler = com_handler
        self.msg_block = msg_block
        self.com_handler.open_connection()
        self.com_handler.send_data(GPS_COMMANDS["DEFINE_LAST_NMEA_SENTENCE"], check_response=True)
        self.com_handler.send_data(GPS_COMMANDS["SET_URC_REPORT"], check_response=True)
        self.com_handler.send_data(GPS_COMMANDS["SEND_GPS_DATA_TO_UART"], check_response=True)

    def run(self):
        """
        Run gps module

        :return:
        """
        try:
            while not self.stop_command:
                self._get_gps_infos()
                time.sleep(0.25)  # secure time sleep
                # write data to
            # self.disable_gps_module()
            # while(True):
            #    self.get_gnss_nav_infos()
        finally:
            self._disable_gps_module()

    def start(self):
        """

        :return:
        """
        self.stop_command = False
        self._enable_gps_module()
        self.run()

    def stop(self):
        """
        Stop command

        :return:
        """
        self.stop_command = True

    def _enable_gps_module(self):
        """
        Set Power to GPS module

        :return:
        """
        self.com_handler.send_data(GPS_COMMANDS["GPS_POWER_ON"], check_response=True)
        self.gps_module_status = GPS_STATUS['ON']

    def _disable_gps_module(self):
        """
        Unset Power to GPS module

        :return:
        """
        # because of data flow it can't be check "normal" response, so response must be checked by regex
        self.com_handler.send_data(GPS_COMMANDS["GPS_POWER_OFF"])
        self.com_handler.check_response_in_data_flow(GPS_COMMANDS["GPS_POWER_OFF"])
        self.gps_module_status = GPS_STATUS['OFF']

    def _get_gps_infos(self):
        """
        Get GPS Infos

        :return: True: if both messages could be read and False: if one or more message blocks are None (no data!)
        :rtype: bool
        """
        # check if gps module power is on
        if self.gps_module_status == GPS_STATUS['OFF']:
            self._enable_gps_module()

        # init values
        utc_time = None
        date = None

        data_buffer = self.com_handler.receive_data()
        # read latitude and longitude
        gngga_data = re.search(GNGGA, data_buffer)
        gnrmc_data = re.search(GNRMC, data_buffer)
        try:
            if gngga_data is not None:
                logging.debug("---Parsing GNGGA---")
                if gngga_data.group(2) == '$GNGGA':
                    utc_time = gngga_data.group(3)  # summer time!!!
                    lat = gngga_data.group(4)
                    self.msg_block.lat = convert_nmea_to_dec(lat)
                    long = gngga_data.group(6)
                    self.msg_block.lng = convert_nmea_to_dec(long)
                else:
                    logging.error("wrong 'GNGGA' data format!")
            # read time and date
            if gnrmc_data is not None:
                logging.debug("---Parsing GNRMC---")
                if gnrmc_data.group(2) == '$GNRMC':
                    date = gnrmc_data.group(11)
                else:
                    logging.error("wrong 'GNRMC' data format!")
            if date is not None and time is not None:
                self.msg_block.timestamp = convert_utc_date_time(utc_time=utc_time, date=date)
        except Exception:
            logging.warning("no satellite found!")
        return bool(gngga_data and gnrmc_data)

    def get_gnss_nav_infos(self):
        """
        Parse CGNSINF data struct

        :return:
        """
        self.com_handler.send_data(GPS_COMMANDS["PRINT_GPS_INFO"])
        data = self.com_handler.receive_data()
        gps_matches = re.findall(gnss_data_struct_pattern, data)
        if len(gps_matches) == 0:
            logging.error("[ERROR] No GPS Signal!")
        for gps_data in gps_matches:
            logging.debug("---------------------------------------------")
            logging.debug("UTC Date Time = %s" % convert_utc_time(gps_data[CGNSINF_Struct.utc_date_time]))
            logging.debug("Latitude is = %s" % gps_data[CGNSINF_Struct.latitude])
            logging.debug("Longitude is = %s" % gps_data[CGNSINF_Struct.longitude])
            logging.debug("GPS Satellites in View = %s" % gps_data[CGNSINF_Struct.gps_satellites_in_view])
            logging.debug("GNSS Satellites Used = %s" % gps_data[CGNSINF_Struct.gnss_satellites_used])
            logging.debug("GLONASS Satellites in View = %s" % gps_data[CGNSINF_Struct.glonass_satellites_in_view])
            logging.debug("Speed = %s" % gps_data[CGNSINF_Struct.speed_over_ground])
            logging.debug("Course = %s" % gps_data[CGNSINF_Struct.course_over_ground])

    # Deleting (Calling destructor)
    def __del__(self):
        self.stop()
        time.sleep(5)  # wait for finishing
        logging.debug('Destructor called, Thread deleted.')
