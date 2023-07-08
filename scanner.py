import time

from beacontools import BeaconScanner, EddystoneTLMFrame
from flask import Flask
from cache import Cache
devices = Cache()
app = Flask(__name__)


@app.route('/temp')
def tempInfo():
    data = devices.getKey(macAddr)
    temp = data["packet"]
    return temp
    
@app.route('/device')
def deviceInfo():
    return devices.getKey(macAddr)
    
@app.route('/')
def info():
    return 'Sensor Server Running'
    
def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    devices.setKey(bt_addr, { "bt_addr": bt_addr, "rssi": rssi, "packet": packet, "additional_info": additional_info })
    
print("Scan Started")
scanner = BeaconScanner(callback)
scanner.start()
app.run(host="0.0.0.0", port="5956")
