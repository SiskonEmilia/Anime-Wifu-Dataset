import cv2
import sys
import os.path

def detect(cascade_file = "../cropper/lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread('shiroha.jpg', cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces_1 = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (16, 16))
    faces_2 = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.5,
                                     minNeighbors = 5,
                                     minSize = (16, 16))

    for i, (x, y, w, h) in enumerate(faces_2):
        cv2.imwrite("cropped.png", image[y:y+h, x:x+w])

    for (x, y, w, h) in faces_1:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (x, y, w, h) in faces_2:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)    

    cv2.imshow("AnimeFaceDetect", image)
    cv2.imwrite("detected.png", image)

detect()