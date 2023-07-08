import time

from beacontools import BeaconScanner, EddystoneTLMFrame

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

scanner = BeaconScanner(callback,
    packet_filter=EddystoneTLMFrame
)
scanner.start()
time.sleep(10)
scanner.stop()