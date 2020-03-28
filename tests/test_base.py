##############################################################################
# For copyright and license notices, see LICENSE file in root directory
##############################################################################
import unittest
from respyrator.core import Core


class TestBase(unittest.TestCase):
    def test(self):
        self.assertTrue(True)

    def test_core(self):
        core = Core()
        self.assertEqual(core.sum(1, 2), 3)
