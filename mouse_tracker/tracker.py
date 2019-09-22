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
    roi = None
    backSub = cv2.createBackgroundSubtractorKNN()
    def __init__(self, videoPath=None, roi=None):
        self.video = cv2.VideoCapture(videoPath)

        if roi:
            print("Atribuindo ROI!")
            self.roi = roi
        print(self.roi)

    def __del__(self):
        self.video.release()

    """ imCrop é do tipo <class 'numpy.ndarray'>
    # Para fazer o crop da imagem é esperado 4 valores na seguinte ordem
    # img[int('Y inicial'):int('Y inicial' + 'Altura'), int('X inicial'):int('X inicial' + 'Largura')]
    """
    def get_frame(self):
        if self.roi:
            ret, frame = self.video.read()

            image_delimited = frame[int(self.roi[1]):int(self.roi[1] + self.roi[3]), int(self.roi[0]):int(self.roi[0] + self.roi[2])]
            
            if frame is None:
                return
            
            #aplica a subtração
            fgMask = self.backSub.apply(image_delimited)
            contours, hierarchy = cv2.findContours(fgMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            #mostra o numero de frames e mais umas coisaradas
            # cv2.putText(frame, str(capture.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
            #         cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
            #desenha o retangulo
            for c in contours:
                if cv2.contourArea(c) < 500:
                    continue
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                continue

            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        # if self.roi:
        #     success, image = self.video.read()
        #     image_delimited = image[int(self.roi[1]):int(self.roi[1] + self.roi[3]), int(self.roi[0]):int(self.roi[0] + self.roi[2])]
            
        #     #APLICA O SUBTRACTOR
        #     mask = subtractor.apply(image_delimited)

        #     #REDUZ O RUIDO COM MORPHOLOGY
        #     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)

        #     #PEGA APENAS O CONTORNO
        #     mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, None)

        #     #DILATA PARA FICAR MAIS FACIL VER (Quanto maior o unumero de iteracoes, maior a dilatacao)
        #     #Poderia colocar o numero de iteracoes editavel
        #     mask = cv2.dilate(mask, None, iterations=12)

        #     #CAPTURA OS CONTORNOS
        #     (contours, hierarchy) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #     #DESENHA OS CONTORNOS
        #     for c in contours:
        #     #Aqui da pra fazer o tratamento de ruido do vídeo

        #         if cv2.contourArea(c) > 2000 and cv2.contourArea(c) < 50000:
        #             (x, y, w, h) = cv2.boundingRect(c)
        #             cv2.rectangle(image_delimited, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #             continue
        #     #SE image FOR NULO, RETORNA UM .jpg VAZIO (Se nao, quando acaba o video da pau em tudo)
        #     ret, jpeg = cv2.imencode('.jpg', image)
        #     return jpeg.tobytes()

        
        else:
            print("roi nao selecionado")
            success, image = self.video.read()
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
    

    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()