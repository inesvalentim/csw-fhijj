import cv2
import numpy

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

i=1
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(200)
    if key == 27: # exit on ESC
        break
    face_cascade = cv2.CascadeClassifier('C:\\Users\\joaof\\PycharmProjects\\test\\haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.circle(frame,(x+w/2,y+h/2),int(w*0.85),(255, 0, 0), 2)

cv2.destroyWindow("preview")

