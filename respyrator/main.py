import os
import subprocess
import sys

import serial
import fakeSerial

from dotenv import load_dotenv

import communications
import collectorPrometheus



load_dotenv(os.path.join(os.path.dirname(__file__), 'settings.env'))

if os.environ.get("FAKE_SERIAL_DEBUGGING") is not None:
    fakeSerialDebugging = bool( os.environ.get("FAKE_SERIAL_DEBUGGING") )
else:
    fakeSerialDebugging = False

if os.environ.get("RESPIRATOR_PORT") is not None:
    masterPort = os.environ.get("RESPIRATOR_PORT")
    if fakeSerialDebugging == True:
        s = fakeSerial.Serial(port=masterPort, baudrate=115200,timeout=0.1)
    else:
        s = serial.Serial(port=masterPort, baudrate=115200,timeout=0.1)
else: 
    raise ValueError("RESPIRATOR_PORT not specified. Use environment variable")

counter = 0

collector = collectorPrometheus.ReespiratorCollector()
collectorPrometheus.REGISTRY.register(collector)

while True:
    collectorPrometheus.start_http_server(8001)
    packet = communications.tx_frame()
    if fakeSerialDebugging == True:
        packet.recv_from(s, blocking=False)
    else:
        packet.recv_from(s)
    packet.print( collector )
    if communications.check_crc(packet):
        print("Packet received correctly")
    else:
        print("WRONG PACKET!!")
    packet.Header = 12
    communications.generate_crc(packet)

    # print("Sending packet with crc:%d" % packet.Crc)
    # communications.send_packet(s,packet)
    
    #print("New Packet received[%d]" % counter)
    #time.sleep(0.5)
    #send_packet(s,p)
    counter = counter +1