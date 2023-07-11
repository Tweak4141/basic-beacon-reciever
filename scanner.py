
import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from beacontools import parse_packet
from quart import Quart, jsonify, websocket
from cache import Cache
from datetime import datetime

devices = Cache()
app = Quart(__name__)

def callback(device: BLEDevice, advertisement_data: AdvertisementData):
    if device.address != "CB:05:8F:EC:67:82":
        return
    print(device, advertisement_data)
    data = advertisement_data.service_data.get(advertisement_data.service_uuids[0])
    url_bytes = b"\x03\x03\xAA\xFE\x13\x16\xAA\xFE" + data 
    parsedData = parse_packet(url_bytes)
    try:
        devices.setKey(str(device.address).lower(), str({ "bt_addr": device.address, "rssi": advertisement_data.rssi, "packet": { "tx_pwr": parsedData.tx_power, "url": parsedData.url.replace("http://","") }, "additional_info": device.name, "date_created": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}))
    except AttributeError as at:
        print(f"Attribute Error. No matching attribute.\nStack Trace:\n{at}")
    except:
        print("Something went wrong")

async def main():
    scanner = BleakScanner(callback)
    while True:
        print("(re)starting scanner")
        await scanner.start()
        await asyncio.sleep(5.0)
        await scanner.stop()

@app.before_serving
async def startup():
    app.add_background_task(main)

@app.route('/temp/<macAddr>')
def tempInfo(macAddr):
    data = devices.getKey(macAddr.lower())
    if not data:
        return "NO DEVICE FOUND", 404
    return jsonify(data)

@app.websocket("/ws/<macAddr>")
async def ws(macAddr):
    while True:
        await websocket.send_json(devices.getKey(macAddr.lower()))

@app.route('/device/<macAddr>')
def deviceInfo(macAddr):
    data = str(devices.getKey(macAddr.lower()))
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
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5956")
