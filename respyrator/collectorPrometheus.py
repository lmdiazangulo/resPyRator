

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
            c.add_metric(['rpm'], self.packet.RPM_measure)
            c.add_metric(['peakPressure'], self.packet.PEAK_pressure_measure)
            c.add_metric(['peepPressure'], self.packet.PEEP_pressure_measure)
            c.add_metric(['flow'], self.packet.Flow_measure)
        # TODO: read from laptop/device
        c.add_metric(['battery'], 60)
        yield c