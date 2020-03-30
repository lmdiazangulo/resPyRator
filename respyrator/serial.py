##############################################################################
# For copyright and license notices, see LICENSE file in root directory
##############################################################################
import os
try:
    import pty
except ImportError:
    pty = None
import serial
import time
import sys
import glob
import threading
from .data_frame import RxFrame, DataFrame


def serial_ports_get():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def serial_port_frame_get(port, timeout=3):
    def test(result, port):
        with serial.Serial(port, timeout=0.1) as s:
            df = DataFrame(s)
            result.append(df.read())

    result = []
    thread = threading.Thread(target=test, args=[result, port])
    thread.daemon = True
    thread.start()
    time.sleep(timeout)
    threading.currentThread().ident
    return result and result[0] or None


def serial_discovery_port():
    ports = serial_ports_get()
    for port in ports:
        frame = serial_port_frame_get(port)
        if frame and isinstance(frame, RxFrame):
            return port
    return None


def serial_get(port):
    return serial.Serial(port=port, baudrate=115200, timeout=0.1)


class FakeSerial:
    def __init__(self, file_name, sleep=0.2):
        self._waiting = True
        master, slave = pty.openpty()
        self.serial = serial.Serial(os.ttyname(slave))
        self.sleep = sleep
        if not os.path.exists(file_name):
            raise Exception(
                'File "%s" with samples frames not exists' % file_name)
        self.file_name = file_name

    @property
    def in_waiting(self):
        return self._waiting

    def read(self, size):
        generator = self.generator(size)
        return next(generator)

    def generator(self, size):
        with open(self.file_name, 'rb') as fp:
            while True:
                byte = fp.read(size)
                if not byte:
                    break
                yield byte
                self._waiting = True
                time.sleep(self.sleep)
                self._waiting = False
