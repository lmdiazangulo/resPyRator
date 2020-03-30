##############################################################################
# For copyright and license notices, see LICENSE file in root directory
##############################################################################
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server


class ReespiratorCollector(object):
    def __init__(self):
        self.packet = None

    def setPacket(self, packet):
        self.packet = packet

    def collect(self):
        c = GaugeMetricFamily('reespirator', 'Reespirator', labels=['vars'])
        if self.packet:
            c.add_metric(['rpm'], self.packet.rpm_measure)
            c.add_metric(['peakPressure'], self.packet.peak_pressure_measure)
            c.add_metric(['peepPressure'], self.packet.peep_pressure_measure)
            c.add_metric(['flow'], self.packet.flow_measure)
        yield c


def init():
    collector = ReespiratorCollector()
    REGISTRY.register(collector)
    start_http_server(8000)


if __name__ == '__main__':
    init()
