import os
import re
import sys
import unittest

""" Integration test: parse the recorded NMEA log (extra/GPS-LOG.txt) with the same
    regex patterns and conversion functions the tracker uses at runtime
"""

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'src'))

from constants import GNGGA, GNRMC
from gps_module import convert_nmea_to_dec


class TestIntegration(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ROOT, 'extra', 'GPS-LOG.txt')) as log_file:
            # line breaks are stored escaped in the log file, restore the real CR LF
            self.lines = [line.strip().replace('\\r\\n', '\r\n') for line in log_file if line.strip()]

    def test_parse_recorded_log(self):
        positions = []
        for line in self.lines:
            gngga = re.search(GNGGA, line)
            gnrmc = re.search(GNRMC, line)
            if gngga and gnrmc and gngga.group(4):
                positions.append((convert_nmea_to_dec(gngga.group(4)), convert_nmea_to_dec(gngga.group(6))))
        self.assertTrue(len(positions) > 0, 'no valid position found in GPS-LOG.txt')
        for lat, lng in positions:
            # all recordings were taken around Deggendorf
            self.assertTrue(48.5 < lat < 49.5)
            self.assertTrue(11.5 < lng < 12.5)


if __name__ == '__main__':
    unittest.main()
