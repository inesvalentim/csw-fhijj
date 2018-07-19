#!/usr/bin/env python

# imports:

from facerekog import *
from flask import Flask, render_template, Response, request
from importlib import import_module
import os
import base64
import cv2
import numpy as np



if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# variables:

app = Flask(__name__)

noSignal = cv2.imread('hugo.jpg', 0)
success, tmpFrame = cv2.imencode('.jpg', noSignal)
tmpFrame = base64.b64encode(tmpFrame).decode()
tmpFrame = base64.b64decode(tmpFrame)
awsFrame = tmpFrame
#awsFrame = None


#faz o treino
path_dir=''
p_fig=['ines1_s',
       'joaoc_s'
       ]
known_face_names=[  "Ines Valentim",
"Joao Carvalho"
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

    pessoas = clientContent[u'objects']
    print pessoas
    global awsFrame
    #se houver pessoas
    if len(pessoas):
    # tratar do resto...

        img0 = base64.b64decode(newframe)
        img2 = rekog(img0,known_face_encodings,known_face_names)

        success, img3 = cv2.imencode('.jpg', img2)
        image = base64.b64encode(img3)
        image_ready = image.decode('utf-8')
        image = base64.b64decode(image_ready)
        #img4= img3.decode()

        awsFrame = image

    #senao nao ha
    else:
        img0 = base64.b64decode(newframe)
        awsFrame = img0

    return Response("ok", mimetype='text')


if __name__ == '__main__':
    # app.run(host='10.8.11.45', threaded=True)
    app.run(host='10.8.11.19', threaded=True)
