import network
import ntptime

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('YOUR_SSID', 'YOUR_KEY')

while not wifi.isconnected():
    pass

print(wifi.ifconfig())

ntptime.settime()

