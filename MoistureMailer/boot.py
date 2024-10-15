import network
import time
import machine

ssid = 'Room-301'
password = 'etrx@301'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())

