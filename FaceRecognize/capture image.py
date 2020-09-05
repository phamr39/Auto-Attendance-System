from imutils.video import VideoStream
from imutils.video import FPS
import cv2
import numpy as np
import  time
vs = VideoStream(src=1).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
tt1 = True
t=0
while tt1 == True:

    t1= str(t)+'.jpg'
    frame = vs.read()
    h=frame.shape[0]
    w=frame.shape[1]
    # frameS = cv2.resize(frame, (720, 960))
    imgS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                      minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
    boxes = np.array(boxes)
    if (len(boxes) != 1):
        cv2.putText(frame, 'khong co ai', (150, 150), cv2.FONT_HERSHEY_SIMPLEX,
                   2, (0,0 , 255), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        continue
    a = int(boxes[:, 0])
    b = int(boxes[:, 1])
    c = int(boxes[:, 2])
    d = int(boxes[:, 3])
    boxes1 = [(a, b, c, d)]


    if ((10 > a or a > 150) or (310 > b or b > 600) or (250 > c or 600 < c) or (60 > d or 300 < d)):
        cv2.putText(frame, 'chua vao dung vi tri', (25, 250), cv2.FONT_HERSHEY_SIMPLEX,
                   1.5, (255, 0, 0), 2)
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
        continue
    else:
        cv2.putText(frame, 'du nguyen vi tri', (250, 250), cv2.FONT_HERSHEY_SIMPLEX,
                   1, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
    time.sleep(1)
    frame = vs.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                      minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
    boxes = np.array(boxes)
    if (len(boxes) != 1):
        continue
    cv2.imwrite(t1,frame)
    cv2.putText(frame, 'da luu', (250, 250), cv2.FONT_HERSHEY_SIMPLEX,
                3, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
    time.sleep(20)
    t = t + 1
    cv2.destroyAllWindows()




