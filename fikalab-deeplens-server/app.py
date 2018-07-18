#!/usr/bin/env python

# imports:

from flask import Flask, render_template, Response
from importlib import import_module
import os
import request
import base64
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# variables:

app = Flask(__name__)

awsFrame = None

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


def ourResponse():
    """Video streaming generator function."""
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + awsFrame.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(ourResponse(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_stream', methods=['PUT'])
def video_stream():
    """Video streaming route. Put this in the src attribute of an img tag."""
    clientContent = request.get_json(silent=True)
    global awsFrame
    awsFrame = base64.b64decode(clientContent['frame'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
