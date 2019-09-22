from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
import numpy as np
import threading
import gzip
import cv2

subtractor = cv2.createBackgroundSubtractorMOG2( detectShadows = False)
test = 0
class Tracker(object):
    def __init__(self, videoPath=None, roi=None):
        self.video = cv2.VideoCapture(videoPath)
        

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
