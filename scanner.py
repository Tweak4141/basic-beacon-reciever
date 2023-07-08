import time

from beacontools import BeaconScanner
from flask import Flask, jsonify
from cache import Cache
from datetime import datetime

devices = Cache()
app = Flask(__name__)
seconds = 10
scanning = False

def restartScan():
    global scanning
    if scanning == False:
       scanner.start()
       scanning = True
       time.sleep(seconds)
       scanner.stop()
       scanning = False
       
@app.route('/temp/<macAddr>')
def tempInfo(macAddr):
    data = devices.getKey(macAddr)
    if not data:
        return "NO DEVICE FOUND", 404
    temp = data["packet"]["url"]
    return jsonify({ "temp": temp.replace("http://",""), "date": data["date_created"] })
    
@app.route('/device/<macAddr>')
def deviceInfo(macAddr):
    data = str(devices.getKey(macAddr))
    if not data:
        return "NO DEVICE FOUND", 404
    return jsonify(data)

@app.route('/updatetime/<sec>')
def updateSeconds(sec):
    global seconds
    seconds = sec
    return seconds
   
@app.route('/')
def info():
    return 'Sensor Server Running'
    
def callback(bt_addr, rssi, packet, additional_info):
    devices.setKey(bt_addr, { "bt_addr": bt_addr, "rssi": rssi, "packet": { "tx_pwr": packet.tx_power, "url": packet.url }, "additional_info": additional_info, "date_created": datetime.now().strftime("%m/%d/%Y, %H:%M:%S") })
    
print("Scan Started")
scanner = BeaconScanner(callback)
app.run(host="0.0.0.0", port="5956")

while True:
    restartScan()

