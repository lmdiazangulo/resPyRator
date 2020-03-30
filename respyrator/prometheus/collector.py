##############################################################################
# For copyright and license notices, see LICENSE file in root directory
##############################################################################
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
)
import respyrator


class ReespiratorCollector:
    def __init__(self):
        self.frame = None

    def frame_set(self, frame):
        self.frame = frame

    def collect(self):
        c = GaugeMetricFamily('reespirator', 'Reespirator', labels=['vars'])
        if self.frame:
            c.add_metric(['rpm'], self.frame.rpm_measure)
            c.add_metric(['peakPressure'], self.frame.peak_pressure_measure)
            c.add_metric(['peepPressure'], self.frame.peep_pressure_measure)
            c.add_metric(['flow'], self.frame.flow_measure)
            self.frame = None
        yield c


def init():
    port = respyrator.serial.serial_discovery_port()
    if not port:
        print('Device Arduino no port found!')
        sys.exit(-1)
    serial = respyrator.serial.serial_get(port)
    df = respyrator.data_frame.DataFrame(serial)
    collector = ReespiratorCollector()
    REGISTRY.register(collector)
    start_http_server(8000)
    while True:
        frame = df.read()
        collector.frame_set(frame)


if __name__ == '__main__':
    init()
