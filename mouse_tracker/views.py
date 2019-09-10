from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
import numpy as np
import threading
import gzip
import cv2

subtractor = cv2.createBackgroundSubtractorMOG2(history = 100,	varThreshold = 8,	detectShadows = False )

# Create your views here.
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        #self.video = cv2.VideoCapture("video.mp4")
        (self.grabbed, self.frame) = self.video.read()
        if self.grabbed == None or self.frame.any() == None:
            print("Deu ruim mano")

        threading.Thread(target=self.update, args=()).start()
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        #Flip Image Horizontally
        image = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

    def desenharCaixa():
        return False


cam = VideoCamera()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



def livefe(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
        #return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass

def stream(request):
    context = {
        'something': "something"
    }
    return render(request, 'mouse_tracker/index.html', context)


## Simple Tracking
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
