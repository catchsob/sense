import os
import argparse
from urllib.request import urlopen

import cv2
import numpy as np


def watch(bufsz=4096, glance=False, ai=False):
    jpghead, jpgend = -1, -1
    bts = stream.read(bufsz)
    while True:
        if jpghead < 0:
            jpghead = bts.find(b'\xff\xd8')
            if jpghead < 0:
                bts = stream.read(bufsz)
                continue
            bts = bts[jpghead:]
            jpghead = 0
        jpgend = bts.find(b'\xff\xd9')
        if jpgend < 0:  # need more data
            if len(bts) < bufsz*4:
                bts += stream.read(bufsz)
            else:  # prevent accident
                jpghead = -1
                bts = stream.read(bufsz) 
        else:
            jpg = bts[jpghead:jpgend+2]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            if ai:
                img = detect(img)
            cv2.imshow('any key to exit', img)
            if glance:
                cv2.waitKey(0)
                break
            elif cv2.waitKey(10) > 0:
                break
            bts = bts[jpgend+2:]
            jpghead, jpgend = -1, -1
            if len(bts) < 100:  # review existing buffer
                bts += stream.read(bufsz)

def detect(img):
    r = haar.detectMultiScale(img, minNeighbors=2, minSize=(10,10))
    for x,y,w,h in r:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0))
    return img


parser = argparse.ArgumentParser()
parser.add_argument("--buffer", "-b", type=int, default=4096, help='buffer size of ESP32CAM stream, default 4096')
parser.add_argument("--glance", "-g", action='store_true', default=False, help='just grab one picture')
parser.add_argument("--haarcascade", "-c", type=str, help='Haar-cascade file to detect someting')
parser.add_argument("--ip", "-i", type=str, default='127.0.0.1', help='IP address of ESP32CAM stream, default 127.0.0.1')
parser.add_argument("--port", "-p", type=int, default=81, help='port of ESP32CAM stream, default 81')
parser.add_argument("--timeout", "-t", type=int, default=2, help='timeout of ESP32CAM stream, default 2 secs')
args = parser.parse_args()
stream = None

try:
    haar = None
    if args.haarcascade and os.path.isfile(args.haarcascade):
        haar = cv2.CascadeClassifier(args.haarcascade)
    url = f'http://{args.ip}:{args.port}/stream'
    stream = urlopen(url, timeout=args.timeout)
    watch(bufsz=args.buffer, glance=args.glance, ai=(haar!=None))
except Exception as e:
    print(f'teminated due to {e}')

if stream:
    stream.close()
cv2.destroyAllWindows()
