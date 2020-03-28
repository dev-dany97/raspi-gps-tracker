import unittest
import sys
import os

""" Example integration test using the unittest framework
    feel free to replace with a test framework of your choice
"""

sys.path.insert(0, '../../@@@PACKAGENAME@@@')


class TestIntegration(unittest.TestCase):
    def test_integration(self):
        # TODO: add some real tests
        self.assertTrue(False, 'Add some integration tests')


if __name__ == '__main__':
    unittest.main()
