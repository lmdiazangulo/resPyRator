import os
import subprocess
import sys
from dotenv import load_dotenv

from collectorPrometheus import *
from communications import *

collector = ReespiratorCollector()

REGISTRY.register(collector)

load_dotenv("settings.env")

if os.environ.get("RESPIRATOR_PORT") is not None:
    masterPort = os.environ.get("RESPIRATOR_PORT")
else: 
    raise ValueError("RESPIRATOR_PORT not specified. Use environment variable")

s = serial.Serial(port=masterPort, baudrate=115200,timeout=0.1)
counter = 0

while True:
    start_http_server(8001)
    packet = recv_packet_blocking(s)
    print_packet(packet)
    if check_crc(packet):
        print("Packet received correctly")
    else:
        print("WRONG PACKET!!")
    packet.Header = 12
    generate_crc(packet)
    print("Sending packet with crc:%d" % packet.Crc)
    send_packet(s,packet)
    #print("New Packet received[%d]" % counter)
    #time.sleep(0.5)
    #send_packet(s,p)
    counter = counter +1