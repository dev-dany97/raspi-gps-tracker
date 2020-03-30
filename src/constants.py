# coding=utf-8
from pip._internal.utils.misc import enum

##### IMPORTANT SETTINGS ######
from typing import Dict, Any, Union

BAUDRATE = 115200  # UART communication bus baud rate
GPS_BAUDRATE = 115200
W_TIMEOUT = 10  # write timeout in sec
R_TIMEOUT = 15  # read timeout in sec
# COMMON_PORT_NAME = "COM3"  # mostly on Windows systems
COMMON_PORT_NAME = "/dev/ttyS0"  # The user UART device of Raspberry Pi 2B/Zero is ttyAMA0, and ttyS0 of Raspberry Pi 3B
ENTER_KEY = '\r\n'

ERROR_STRING = 'ERROR' + ENTER_KEY
OK_STRING = 'OK' + ENTER_KEY

# SIM Card constants (GPRS Commands)
SIM_CARD_COMMANDS = {
    "GPRS_NET_LOG_IN": "AT+CGATT?",  # GPRS-Netz eingebucht? (1 -> eingebucht, 0 -> nicht eingebucht)
    "SET_APN": "AT+SAPBR=3,1,\"APN\",\"TM\"",
    "OPEN_GPRS_CONTEXT": "AT+SAPBR=1,1",  # GPRS-Kontext oeffnen; LED blinkt dann sehr rasch
    "USER_REQUEST": "AT+SAPBR=2,1",  # Nutzer-Anfrage
    "INIT_HHTP_SERVICE": "AT+HTTPINIT",  # HTTP-Dienst initialisieren
    "SET_HTTP_URL": "AT+HTTPPARA=\"URL\",\"http://industrial.api.ubidots.com/api/v1.6/devices/raspberryPiGPSTracker\"",
    # HTTP-Parameter setzen: URL angeben
    "SET_HTTP_USERDATA": "AT+HTTPPARA=\"USERDATA\",\"X-Auth-Token: YOUR-UBIDOTS-TOKEN\"",
    # HTTP-Parameter setzen: Userdata angeben
    "SET_HTTP_CONTENT": "AT+HTTPPARA=\"CONTENT\",\"application/json\"",
    # HTTP-Parameter setzen: Http Content typ angeben
    "SET_HTTP_DATA": "AT+HTTPDATA=192,1000",
    # Set Size in bytes of the data to POST and
    # the maximum time in milliseconds to input data (only between 1000-120000 (millisecond))
    "SEND_GET_REQ": "AT+HTTPACTION=0",  # Abfrage starten (0->GET)
    "SEND_POST_REQ": "AT+HTTPACTION=1",  # Upload starten (1->POST)
    "READ_HTTP_ANSWER": "AT+HTTPREAD",  # Antwort des HTTP-Servers lesen
    "SHUTDOWN_HTTP_SERVICE": "AT+HTTPTERM",  # HTTP-Dienst beenden
    "CLOSE_GPRS_CONTEXT": "AT+SAPBR=0,1"  # GPRS-Kontext schliessen; LED blinkt dann wieder im 3-s-Rhythmus
}  # type: Dict[Union[str, Any], Union[str, Any]]

# GPS constants
CGNSINF_Struct = enum('all_data', 'gnss_run_status', 'fix_status', 'utc_date_time', 'latitude', 'longitude',
                      'msl_altitude', 'speed_over_ground', 'course_over_ground', 'fix_mode', 'reserved1', 'hdop',
                      'pdop', 'vdop', 'reserved2', 'gps_satellites_in_view', 'gnss_satellites_used',
                      'glonass_satellites_in_view', 'reserved3', 'c_n0_max', 'hpa', 'vpa')

GPS_COMMANDS = {
    "GPS_POWER_ON": "AT+CGNSPWR=1",  # Turn on the power of GPS
    "GPS_POWER_OFF": "AT+CGNSPWR=0",  # Turn off the power of GPS
    "SET_GPS_BAUDRATE": "AT+CGNSIPR=" + str(GPS_BAUDRATE),  # Set the baud rate of GPS
    "SEND_GPS_DATA_TO_UART": "AT+CGNSTST=1",  # Send data received to UART
    "STOP_GPS_DATA_TO_UART": "AT+CGNSTST=0",  # Stop sending data received to UART
    "DEFINE_LAST_NMEA_SENTENCE": "AT+CGNSSEQ=\"RMC\"",  # Define the last NMEA sentence that parsed.
    # "RMC" refer to "GPRMC", "GLRMC" or "GNRMC"
    "PRINT_GPS_INFO": "AT+CGNSINF",  # GNSS navigation information parsed from NMEA sentences
    "SET_URC_REPORT": "AT+CGNSURC=40",  # GNSS navigation, GEO-fences and speed alarm URC report.
    # Turn on navigation data URC report, and report every 40 GNSS FIX
}

GPS_STATUS = {
    'ON': 1,
    'OFF': 0
}

INTRO_HEADER = '''
         █████      ████████═╗  ███████╗
        ██╗         ██     ██║  ██╔════╝
        ██║  ████╗  ██ █████╔╝  ███████╗
        ██║    ██║  ██╔═════╝   ╚════██║
         ███████╔╝  ██║         ███████║
         ╚══════╝   ╚═╝         ╚══════╝
    created by Daniel Mohles
    '''


class bcolors:
    HEADER = '\033[95m'
    SENDER = '\033[94m'
    RECEIVER = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'


# Regex GPS
GNGGA = '((\$GNGGA),([0-9.]*),([0-9.]{0,11}),([N,E,O,W]?),([0-9.]{0,12}),([N,E,O,W,]?),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)(\\r\\n\$GPGSA))'
GPGSA = '((\$GPGSA),(.*)(\\r\\n\$GLGSA))'
GPGSV = '((\$GPGSV),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)(\\r\\n\$GPGSV))'
GNVTG = '((\$GNVTG),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)(\\r\\n))'
GNRMC = '((\$GNRMC),([0-9.]{0,10}),(.*),([0-9.]{0,11}),([N,S]?),([0-9.]{0,12}),([E,W]?),(.*),(.*),(.*),(.*),(.*),(.*)(\\r\\n\$GNVTG))'

# READ data response <HTTP method specification, HTTP Status Code ,data length>
DATA_RESPONSE_REGEX = '\\+HTTPACTION: 1,([0-9]{3}),([0-9]*)'

# APN data
GPRS_APN = "TN"  # replace with your GPRS APN
GPRS_LOGIN = "login"  # replace with your GPRS login
GPRS_PASSWORD = "password"  # replace with your GPRS password
