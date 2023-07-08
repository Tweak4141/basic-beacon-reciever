import time

from beacontools import BeaconScanner, EddystoneTLMFrame

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
print("Scan Started")
scanner = BeaconScanner(callback)
scanner.start()

