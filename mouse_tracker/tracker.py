from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
import numpy as np
import threading
import time
import gzip
import cv2

subtractor = cv2.createBackgroundSubtractorMOG2( detectShadows = False)
test = 0
class Tracker(object):
    roi = None
    backSub = cv2.createBackgroundSubtractorKNN()
    centerX = 0
    centerY = 0
    minRangeY = 0
    maxRangeY = 0
    minRangeX = 0
    maxRangeX = 0
    firstFrame = None
    confirmCima = 0
    confirmBaixo = 0
    confirmDireita = 0
    confirmEsquerda = 0
    confirmCentro = 0
    isCima = False
    isBaixo = False
    isDireita = False
    isEsquerda = False
    isCentro = True

    def __init__(self, videoPath=None, roi=None):
        self.video = cv2.VideoCapture(videoPath)
        fps = self.video.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count/fps

        print('fps = ' + str(fps))
        print('number of frames = ' + str(frame_count))
        print('duration (S) = ' + str(duration))
        minutes = int(duration/60)
        seconds = duration%60
        print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))

        if roi:
            print("Atribuindo ROI!")
            self.roi = roi
            self.centerX = self.roi[2] / 2
            self.centerY = self.roi[3] / 2
            self.minRangeX = self.centerX - ( self.centerX * 7.5 ) / 100 
            self.maxRangeX = self.centerX + ( self.centerX * 7.5 ) / 100 
            self.minRangeY = self.centerY - ( self.centerY * 7.5 ) / 100 
            self.maxRangeY = self.centerY + ( self.centerY * 7.5 ) / 100 


            print("Largura: {}".format(self.roi[2]))
            print("Altura: {}".format(self.roi[3]))
            print("Centro Y:{}".format(self.centerY))
            print("Centro X:{}".format(self.centerX))
            print("Inicio Faixa Y:{}".format(self.minRangeY))
            print("Fim Faixa Y:{}".format(self.maxRangeY))
            print("Inicio Faixa X:{}".format(self.minRangeX))
            print("Fim Faixa X:{}".format(self.maxRangeX))
            print("Centro X:{}".format(self.centerX))
            print("Altura %s" % (self.roi[3]))
            print("Width %s" % (self.roi[2]))

    def __del__(self):
        self.video.release()

    """ imCrop é do tipo <class 'numpy.ndarray'>
    # Para fazer o crop da imagem é esperado 4 valores na seguinte ordem
    # img[int('Y inicial'):int('Y inicial' + 'Altura'), int('X inicial'):int('X inicial' + 'Largura')]
    """
    def get_frame(self):
        if self.roi:
            start_time = time.clock()
            
            ret, frame = self.video.read()
            image_delimited = frame[int(self.roi[1]):int(self.roi[1] + self.roi[3]), int(self.roi[0]):int(self.roi[0] + self.roi[2])]
            
            if frame is None:
                return

            # gray = cv2.cvtColor(image_delimited, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(image_delimited, (11, 11), 0)
            
            #aplica a subtração
            fgMask = self.backSub.apply(gray)
            thresh = cv2.threshold(fgMask, 0, 200, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            # thresh = cv2.erode(thresh, None, iterations=2)
            contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            # if not contours:
            #     print("Nada sendo detectado!")
            #desenha o retangulo
            for c in contours:
                if cv2.contourArea(c) < 500:
                    continue
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if self.isCentro:
                    if self.minRangeY <= cY <= self.maxRangeY and self.minRangeX <= cX <= self.maxRangeX:
                        cv2.circle(image_delimited, (cX, cY), 7, (255, 0, 0), -1)
                else:
                    cv2.circle(image_delimited, (cX, cY), 7, (255, 0, 0), -1)
                # print("Center %s" % (str(M)))
                (x, y, w, h) = cv2.boundingRect(c)
                if h * w > 7600:
                    continue
                
                if self.minRangeY <= cY <= self.maxRangeY and self.minRangeX <= cX <= self.maxRangeX:
                    self.confirmCentro += 1
                    if self.confirmCentro == 3:
                        # print(time.clock())
                        self.isCentro = True
                        self.isBaixo = False
                        self.isCima = False
                        self.isDireita = False
                        self.isEsquerda = False
                        self.confirmCima = 0
                        self.confirmDireita = 0
                        self.confirmEsquerda = 0
                        self.confirmBaixo = 0
                        # print("Centro")
                        # self.triggerTimer("centro")

                elif cY > self.centerY + 30 and self.minRangeX <= cX <= self.maxRangeX:
                    self.confirmBaixo += 1
                    if self.confirmBaixo == 2:
                        # print(time.clock())
                        self.isBaixo = True
                        self.isCima = False
                        self.isDireita = False
                        self.isEsquerda = False
                        self.isCentro = False
                        self.confirmCima = 0
                        self.confirmDireita = 0
                        self.confirmEsquerda = 0
                        self.confirmCentro = 0
                        # self.triggerTimer("centro")
                        # print("Baixo")

                elif cY < self.centerY - 30 and self.minRangeX <= cX <= self.maxRangeX:
                    self.confirmCima += 1
                    if self.confirmCima == 3:
                        # print(time.clock())
                        self.isCima = True
                        self.isBaixo = False
                        self.isDireita = False
                        self.isEsquerda = False
                        self.isCentro = False
                        self.confirmBaixo = 0
                        self.confirmDireita = 0
                        self.confirmEsquerda = 0
                        self.confirmCentro = 0
                        # self.triggerTimer("centro")
                        # print("Cima")

                elif cX > self.centerX + 30 and self.minRangeY <= cY <= self.maxRangeY:
                    self.confirmDireita += 1
                    if self.confirmDireita == 3:
                        # print(time.clock())
                        self.isDireita = True
                        self.isBaixo = False
                        self.isCima = False
                        self.isEsquerda = False
                        self.isCentro = False
                        self.confirmCima = 0
                        self.confirmBaixo = 0
                        self.confirmEsquerda = 0
                        self.confirmCentro = 0
                        # self.triggerTimer("centro")
                        # print("Direita")
                
                elif cX < self.centerX - 30 and self.minRangeY <= cY <= self.maxRangeY:
                    self.confirmEsquerda += 1
                    if self.confirmEsquerda == 3:
                        # print(time.clock())
                        self.isEsquerda = True
                        self.isBaixo = False
                        self.isCima = False
                        self.isDireita = False
                        self.confirmCima = 0
                        self.confirmBaixo = 0
                        self.confirmDireita = 0
                        self.confirmCentro = 0
                        # self.triggerTimer("centro")
                        # print("Esquerda")

                cv2.rectangle(image_delimited, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                continue
            # print(time.clock() - start_time, "seconds")
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        # if self.roi:
        #     success, image = self.video.read()
        #     image_delimited = image[int(self.roi[1]):int(self.roi[1] + self.roi[3]), int(self.roi[0]):int(self.roi[0] + self.roi[2])]
            
        #     #APLICA O SUBTRACTOR
        #     mask = subtractor.apply(image)

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
        #             cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
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

    def triggerTimer(location):
        print("Chamou função")
        return
        # return JsonResponse({'direction': str(location)})

# tempo no centro
# numero sde cruzamento no centro
# porcentagem de permanencia em cada braço
