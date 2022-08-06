from time import sleep, localtime, time

from machine import Pin
from dht import DHT11
from umqtt.simple import MQTTClient

import esp
esp.osdebug(None)

mqtt_broker = 'YOUR_BROKER'
mqtt_client = MQTTClient(client_id='YOUR_CLIENT', server=mqtt_broker)

p = DHT11(Pin(YOUR_PIN))

while True:
    mqtt_client.connect()
    p.measure()
    temp = p.temperature()
    hum = p.humidity()
    dt = localtime(time() + 28800)
    dt = f'{dt[0]:04}{dt[1]:02}{dt[2]:02}-{dt[3]:02}{dt[4]:02}{dt[5]:02}'
    topic = 'plant/soya/dht11/1'
    content = f'{topic}|{dt}|{temp}|{hum}'
    print(content)
    mqtt_client.publish(topic, content)
    mqtt_client.disconnect()
    sleep(YOUR_SECS)

