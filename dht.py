def detect(dht):
    from time import sleep
    
    while dht:
        try:
            temp = f'{dht.temperature}°C' if dht.temperature else None
            humd = f'{dht.humidity}%' if dht.humidity else None
            print(f"溫度 {temp}/ 濕度: {humd}")
            sleep(1)
        except RuntimeError as e1:
            print(e1)
        except Exception as e2:
            dht.exit()
            raise e2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dht', type=int, choices=[11, 22], default=11,
                    help='sensor type of DHT, default 11')
parser.add_argument('-g', '--gpio', type=int, default=17, help='number of GPIO PIN, default 17')
args = parser.parse_args()

import board
from adafruit_dht import DHT11, DHT22

dht = eval(f'DHT{args.dht}(board.D{args.gpio})')
print(f'set DHT{args.dht} on GPIO {args.gpio}')
detect(dht)
