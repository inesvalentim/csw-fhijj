#!/usr/bin/env python

# imports:
from face_rekog import *
from flask import Flask, render_template, Response, request
from importlib import import_module
import os
import base64
import cv2
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

    decoded_frame=base64.b64decode(newframe)

    img = cv2.imdecode(np.fromstring(newframe, dtype=np.uint8), -1)

    #rekog(img,)
    final = img

     success, jpeg = cv2.imencode('.jpg', final)

    global awsFrame
    awsFrame = final

    # tratar do resto...

    return Response("ok", mimetype='text')


if __name__ == '__main__':
    app.run(host='10.8.11.45', threaded=True)
