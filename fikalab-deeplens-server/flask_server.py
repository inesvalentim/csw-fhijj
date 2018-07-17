import cv2

from flask import Flask, render_template, Response

app = Flask(__name__)

Images = []


@app.route("/hello_world")
def hello():
    return "Hello World!"


def im_loop():
    i = 0
    while i < 3:
        im = cv2.imread("pic{}.jpg".format(i), 0)
        Images.append(im)
        i = i+1

    i = 0
    while True:

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + Images[i].tobytes() + b'\r\n')
        i = (i+1) % 3


def aws_lens():
    """
    while True:
    frame = camera.get_frame()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    :return:
    """


@app.route('/video_feed')
def video_feed():
    return Response(im_loop(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run()


# ler imagens (opencv)
# loop das ftos
# apresenta-las com o localhost

# client envia pedido post c/ imagem
# apresenta-la

# https://blog.miguelgrinberg.com/post/video-streaming-with-flask
