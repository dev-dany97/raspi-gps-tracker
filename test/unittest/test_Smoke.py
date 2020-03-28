import unittest
import sys
import os

sys.path.insert(0, '../../@@@PACKAGENAME@@@')


class TestSmoke(unittest.TestCase):
    def test_smoke(self):
        # TODO: add some real tests
        self.assertTrue(False, 'Add some tests')


if __name__ == '__main__':
    unittest.main()
