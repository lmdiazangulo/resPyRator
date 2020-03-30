##############################################################################
# For copyright and license notices, see LICENSE file in root directory
##############################################################################
from respyrator.data_frame import RxFrame, DataFrame
from respyrator.serial import FakeSerial
import os
import unittest


class TestDataFrame(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def path(self, *args):
        return os.path.join(os.path.dirname(__file__), 'samples', *args)

    def test_tx_frame(self):
        self.assertEqual(RxFrame.sizeof(), 42)

    def test_fake_serial(self):
        fname = self.path('1_frame.data')
        with open(fname, 'rb') as fp:
            file_content = fp.read(RxFrame.sizeof())
        serial = FakeSerial(fname)
        serial_frame = serial.read(RxFrame.sizeof())
        self.assertEqual(serial_frame, file_content)

    def test_dataframe(self):
        fname = self.path('1_frame.data')
        serial = FakeSerial(fname)
        df = DataFrame(serial)
        frame = df.read()
        self.assertEqual(frame.header, 0x44)
        self.assertIn('Header', str(frame))
        self.assertIn('Peak pressure setting', str(frame))
