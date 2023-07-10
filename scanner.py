import time

from beacontools import BeaconScanner, EddystoneURLFrame
from flask import Flask, jsonify
from cache import Cache
from datetime import datetime

devices = Cache()
app = Flask(__name__)
seconds = 60
scanning = False


def main(restart):
    scanner: BeaconScanner = BeaconScanner(callback, packet_filter=[EddystoneURLFrame])
    if restart:
        scanner.stop()
        time.sleep(1)
    scanner.start()

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

@app.route('/restart')
def restart():
    main(True)

@app.route('/')
def info():
    return 'Sensor Server Running'
    
def callback(bt_addr, rssi, packet, additional_info):
    print(bt_addr)
    try:
        devices.setKey(bt_addr, { "bt_addr": bt_addr, "rssi": rssi, "packet": { "tx_pwr": packet.tx_power, "url": packet.url }, "additional_info": additional_info, "date_created": datetime.now().strftime("%m/%d/%Y, %H:%M:%S") })
    except AttributeError as at:
        print(f"Attribute Error. No matching attribute.\nStack Trace:\n{at}")
    except:
        print("Something went wrong")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5956")
    main()