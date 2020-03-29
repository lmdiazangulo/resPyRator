from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server

class ReespiratorCollector(object):
    def collect(self):
        c = GaugeMetricFamily('reespirator', 'Reespirator', labels=['vars'])
        # TODO: Read real values from serial port
        c.add_metric(['rpm'], 12)
        c.add_metric(['peakPressure'], 28)
        c.add_metric(['peepPressure'], 6)
        c.add_metric(['flow'], 3)
        c.add_metric(['battery'], 60)
        yield c

REGISTRY.register(ReespiratorCollector())

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8001)
    while True:
        pass
