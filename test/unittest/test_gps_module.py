import os
import sys
import unittest
from datetime import datetime

try:
    from unittest import mock
except ImportError:  # python 2
    import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from gps_module import GPS, convert_nmea_to_dec, convert_utc_date_time
from message import Message

# recorded sample from extra/GPS-LOG.txt (as received from the module, with real CR LF)
NMEA_SAMPLE = '$GNGGA,160713.000,4901.939124,N,01205.934798,E,2,11,0.94,336.018,M,47.297,M,,*78\r\n' \
              '$GPGSA,A,3,29,25,21,31,26,05,,,,,,,1.29,0.94,0.88*09\r\n' \
              '$GLGSA,A,3,83,82,66,80,73,,,,,,,,1.29,0.94,0.88*14\r\n' \
              '$GNRMC,160713.000,A,4901.939124,N,01205.934798,E,0.00,90.42,220320,,,D*4F\r\n' \
              '$GNVTG,90.42,T,,M,0.00,N,0.00,K,D*19\r\n'

NO_FIX_SAMPLE = '$GNGGA,155214.089,,,,,0,0,,,M,,M,,*51\r\n$GPGSA,A,1,,,,,,,,,,,,,,,*1E\r\n' \
                '$GLGSA,A,1,,,,,,,,,,,,,,,*02\r\n$GPGSV,1,1,04,29,,,49,18,,,40,21,,,43,31,,,47*73\r\n' \
                '$GLGSV,1,1,02,83,,,36,82,,,37*67\r\n$GNRMC,155214.089,V,,,,,0.00,0.00,060180,,,N*5B\r\n' \
                '$GNVTG,0.00,T,,M,0.00,N,0.00,K,N*2C\r\n'


class TestConvertNmeaToDec(unittest.TestCase):
    def test_latitude(self):
        self.assertAlmostEqual(convert_nmea_to_dec('4901.939124'), 49.0323187, places=6)

    def test_longitude(self):
        self.assertAlmostEqual(convert_nmea_to_dec('01205.934798'), 12.0989133, places=6)

    def test_invalid_coordinate_returns_none(self):
        self.assertIsNone(convert_nmea_to_dec(''))
        self.assertIsNone(convert_nmea_to_dec('abc'))


class TestConvertUtcDateTime(unittest.TestCase):
    def test_winter_time(self):
        local = convert_utc_date_time(utc_time='160713.000', date='220320')
        self.assertEqual(local.replace(tzinfo=None), datetime(2020, 3, 22, 17, 7, 13))
        self.assertEqual(local.utcoffset().total_seconds(), 3600)

    def test_summer_time(self):
        local = convert_utc_date_time(utc_time='120000.000', date='120420')
        self.assertEqual(local.replace(tzinfo=None), datetime(2020, 4, 12, 14, 0, 0))
        self.assertEqual(local.utcoffset().total_seconds(), 7200)


class TestGPS(unittest.TestCase):
    def setUp(self):
        # skip the 5 sec wait in the destructor
        self.sleep_patcher = mock.patch('gps_module.time.sleep')
        self.sleep_patcher.start()
        self.com_handler = mock.MagicMock()
        self.msg_block = Message()
        self.gps = GPS(self.com_handler, self.msg_block)

    def tearDown(self):
        del self.gps
        self.sleep_patcher.stop()

    def test_init_configures_module(self):
        self.com_handler.open_connection.assert_called_once_with()
        self.assertEqual(self.com_handler.send_data.call_count, 3)

    def test_get_gps_infos_parses_position(self):
        self.com_handler.receive_data.return_value = NMEA_SAMPLE
        self.assertTrue(self.gps._get_gps_infos())
        self.assertAlmostEqual(self.msg_block.lat, 49.0323187, places=6)
        self.assertAlmostEqual(self.msg_block.lng, 12.0989133, places=6)

    def test_get_gps_infos_without_fix_keeps_last_position(self):
        self.com_handler.receive_data.return_value = NO_FIX_SAMPLE
        self.gps._get_gps_infos()
        self.assertEqual(self.msg_block.lat, 0)
        self.assertEqual(self.msg_block.lng, 0)


if __name__ == '__main__':
    unittest.main()
