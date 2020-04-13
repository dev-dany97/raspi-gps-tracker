import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from message import Message


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.msg = Message()

    def test_default_values(self):
        self.assertIsNone(self.msg.timestamp)
        self.assertEqual(self.msg.lat, 0)
        self.assertEqual(self.msg.lng, 0)

    def test_set_coordinates(self):
        self.msg.lat = 49.0323187
        self.msg.lng = 12.0989133
        self.assertEqual(self.msg.lat, 49.0323187)
        self.assertEqual(self.msg.lng, 12.0989133)

    def test_set_timestamp(self):
        self.msg.timestamp = 27032020111260
        self.assertEqual(self.msg.timestamp, 27032020111260)

    def test_invalid_latitude_raises(self):
        with self.assertRaises(ValueError):
            self.msg.lat = "49.03"

    def test_invalid_longitude_raises(self):
        with self.assertRaises(ValueError):
            self.msg.lng = 12

    def test_invalid_timestamp_raises(self):
        with self.assertRaises(ValueError):
            self.msg.timestamp = "2020-03-27"

    def test_getting_msg(self):
        self.msg.lat = 51.013432
        self.msg.lng = 12.101624
        self.msg.timestamp = 27032020111260
        self.assertEqual(self.msg.getting_msg(),
                         {'lat': 51.013432, 'lng': 12.101624, 'timestamp': '27032020111260'})


if __name__ == '__main__':
    unittest.main()
