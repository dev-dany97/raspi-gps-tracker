import os
import sys
import unittest

try:
    from unittest import mock
except ImportError:  # python 2
    import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

# pyserial is not needed for these tests
try:
    import serial  # noqa: F401
except ImportError:
    sys.modules['serial'] = mock.MagicMock()

from uart_communication import convert_to_ascii_format


class TestConvertToAsciiFormat(unittest.TestCase):
    def test_line_endings_are_escaped(self):
        self.assertEqual(convert_to_ascii_format('AT\r\nOK\r\n'), 'AT\\r\\nOK\\r\\n')

    def test_plain_text_is_unchanged(self):
        self.assertEqual(convert_to_ascii_format('AT+CGNSINF'), 'AT+CGNSINF')


if __name__ == '__main__':
    unittest.main()
