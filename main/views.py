from django.shortcuts import render
from .models import *
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import os

FACE_DETECTOR_PATH = "{base_path}/frontal face.xml".format(base_path=os.path.abspath(os.path.dirname(__file__)))

@gzip.gzip_page
def With_0(request):
    try: 
        cam = VideoCamera_0()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, '0.html')

@gzip.gzip_page
def With_1(request):
    try:  
        cam = VideoCamera_1()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, '1.html')

#to capture video class
class VideoCamera_0(object):
    def __init__(self):
        
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        
    def __del__(self):
        self.video.release()

    def get_frame(self):
     
        image = self.frame
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        canvas = detect(gray, image)
        canvas=image
        _, jpeg = cv2.imencode('.jpg', canvas)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
    
#to capture video class
class VideoCamera_1(object):
    def __init__(self):
        
        self.video = cv2.VideoCapture(1)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        
    def __del__(self):
        self.video.release()

    def get_frame(self):
     
        image = self.frame
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        canvas = detect(gray, image)
        canvas=image
        _, jpeg = cv2.imencode('.jpg', canvas)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
    
#For detection
def detect(gray, frame) :  
    face_cascade = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray[y:y+h, x:x+w] 
        roi_color = frame[y:y+h, x:x+w]

    return frame

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

