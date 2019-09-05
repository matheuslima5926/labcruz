from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
import numpy as np
import threading
import gzip
import cv2

subtractor = cv2.createBackgroundSubtractorMOG2( detectShadows = False)

# Create your views here.
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture("video.mp4")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
 
        #SE image FOR NULO, RETORNA UM .jpg VAZIO (Se nao, quando acaba o video da pau em tudo)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()
  
cam = VideoCamera()

def gen(camera):
    while True:
        frame = cam.get_frame()
     
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def livefe(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except:  
        pass

def stream(request):
    context = {
        'something': "something"
    }
    return render(request, 'mouse_tracker/index.html', context)