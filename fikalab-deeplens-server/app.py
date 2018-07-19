#!/usr/bin/env python

# imports:

from face_rekog import *
from flask import Flask, render_template, Response, request
from importlib import import_module
import os
import base64
import cv2
from face_rekog import *

if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# variables:

app = Flask(__name__)

noSignal = cv2.imread('nosignal.jpg', 0)
success, tmpFrame = cv2.imencode('.jpg', noSignal)

awsFrame = tmpFrame
#awsFrame = None


#faz o treino
path_dir='images/'
p_fig=['ines1_s',
       'joaoc_s',
       'hugo']
known_face_names=[  "Ines Valentim",
"Joao Carvalho",
"Hugo Marques"
]

known_face_encodings=[]
for i in range(len(p_fig)):
    known_face_encodings.append(encode(path_dir+p_fig[i]+'.jpg'))

# methods:


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(ourResponse(), mimetype='multipart/x-mixed-replace; boundary=frame')


def ourResponse():
    """Video streaming generator function."""
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + awsFrame + b'\r\n')


@app.route('/video_stream', methods=['PUT'])
def video_stream():
    """Video streaming route. Put this in the src attribute of an img tag."""
    clientContent = request.json
    newframe = clientContent[u'frame']

    img0 = base64.b64decode(newframe)

    img1 = cv2.imdecode(np.fromstring(img0, dtype=np.uint8), -1)

    img2 = rekog(img1,known_face_encodings,known_face_names)

    success, img3 = cv2.imencode('.jpg', img2) 

    global awsFrame
    awsFrame = img2

    # tratar do resto...

    return Response("ok", mimetype='text')


if __name__ == '__main__':
    app.run(host='10.8.11.45', threaded=True)
