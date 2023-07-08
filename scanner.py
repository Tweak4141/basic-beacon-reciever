import time

from beacontools import BeaconScanner
from flask import Flask
from cache import Cache
devices = Cache()
app = Flask(__name__)


@app.route('/temp/<macAddr>')
def tempInfo(macAddr):
    data = devices.getKey(macAddr)
    if not data:
        return "NO DEVICE FOUND", 404
    temp = data["packet"]
    return str(temp.url.replace("http://",""))
    
@app.route('/device/<macAddr>')
def deviceInfo(macAddr):
    data = str(devices.getKey(macAddr))
    if not data:
        return "NO DEVICE FOUND", 404
    return str(data)
    
@app.route('/')
def info():
    return 'Sensor Server Running'
    
def callback(bt_addr, rssi, packet, additional_info):
    devices.setKey(bt_addr, { "bt_addr": bt_addr, "rssi": rssi, "packet": packet, "additional_info": additional_info })
    
print("Scan Started")
scanner = BeaconScanner(callback)
scanner.start()
app.run(host="0.0.0.0", port="5956")
