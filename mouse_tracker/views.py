from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.template import loader
import numpy as np
import threading
import gzip
import cv2

subtractor = cv2.createBackgroundSubtractorMOG2( detectShadows = False)
test = 0
# Create your views here.
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture("video.mp4")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

    #APLICA O SUBTRACTOR
        mask = subtractor.apply(image)

    #REDUZ O RUIDO COM MORPHOLOGY
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)

    #PEGA APENAS O CONTORNO
        mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, None)

    #DILATA PARA FICAR MAIS FACIL VER (Quanto maior o unumero de iteracoes, maior a dilatacao)
    #Poderia colocar o numero de iteracoes editavel
        mask = cv2.dilate(mask, None, iterations=12)

    #CAPTURA OS CONTORNOS
        (contours, hierarchy) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #DESENHA OS CONTORNOS
        for c in contours:
    #Aqui da pra fazer o tratamento de ruido do vídeo
        
            if cv2.contourArea(c) > 2000 and cv2.contourArea(c) < 50000:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                continue
    #SE image FOR NULO, RETORNA UM .jpg VAZIO (Se nao, quando acaba o video da pau em tudo)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    

    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()

  
cam = VideoCamera()


def gen(camera):
    try:
        while True:
            frame = cam.get_frame()
        
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + 
            b'\r\n\r\n')
    except:
        return


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


def get_area_selected(request):
    initX = request.POST.get('initX')
    initY = request.POST.get('ínitY')
    areaW = request.POST.get('areaWidth')
    areaH = request.POST.get('areaHeight')
    print("ROI area: Initial X: %s, Initial Y: %s, Width: %s, Height: %s" % (initX, initY, areaW, areaH))
    data = {}
    return JsonResponse(data)
   
    

