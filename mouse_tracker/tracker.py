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
    roiInitX = 0
    roiInitY = 0
    roiEndX = 0
    roiEndY = 0
    rangeVerticalInitX = 0
    rangeVerticalInitY = 0
    rangeVerticalEndX = 0
    rangeVerticalEndY = 0
    rangeHorizontalInitX = 0
    rangeHorizontalInitY = 0
    rangeHorizontalEndX = 0
    rangeHorizontalEndY = 0

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
    tempoTotalCima = 0.0
    tempoTotalBaixo = 0.0
    tempoTotalEsquerda = 0.0
    tempoTotalDireita = 0.0
    tempoTotalCentro = 0.0
    totalBracosAbertos = 0
    totalBracosFechados = 0
    totalCruzamentos = 0
    timerStartado = 0
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
            self.roiInitX = int(self.roi[0])
            self.roiInitY = int(self.roi[1])
            self.roiEndX = int(self.roi[2])
            self.roiEndY = int(self.roi[3])
            self.centerX = self.roiEndX / 2
            self.centerY = int(self.roi[3]) / 2
            self.minRangeX = int(self.centerX) - ( int(self.roi[2]) * 7.5 ) / 100 
            self.maxRangeX = int(self.centerX) + ( int(self.centerX) * 7.5 ) / 100 
            self.minRangeY = int(self.centerY) - ( int(self.centerY) * 7.5 ) / 100 
            self.maxRangeY = int(self.centerY) + ( int(self.centerY) * 7.5 ) / 100 

            self.rangeVerticalInitX = self.roiInitX + self.centerX - self.centerX * 9 / 100
            self.rangeVerticalEndX = int(self.roiInitX) + int(self.centerX) + int(self.centerX) * 9 / 100

            self.rangeVerticalInitY = int(self.roi[1])
            self.rangeVerticalEndY = int(self.roi[3])

            self.rangeHorizontalInitX = self.roiInitX
            self.rangeHorizontalInitY = int(self.roiInitY) + int(self.centerY) - int(self.centerY) * 11 / 100

            self.rangeHorizontalEndX = self.roiInitX + self.roiEndX
            self.rangeHorizontalEndY = int(self.roiInitY) + int(self.centerY) + int(self.centerY) * 11 / 100


            print("Meio da ROI: %s" % (self.rangeVerticalInitX))

            print("Inicio ROI X:{}".format(self.roiInitX))
            print("Inicio ROI Y:{}".format(self.roiInitY))
            print("Fim ROI X:{}".format(self.roiEndX))
            print("Fim ROI Y:{}".format(self.roiEndY))

            print("Centro X:{}".format(self.centerX))
            print("Centro Y:{}".format(self.centerY))


            print("Faixa Vertical Inicio X: %s" % (int(self.roiInitX) + int(self.centerX) - int(self.centerX) * 7.5 / 100))
            print("Faixa Vertical Fim X: %s" % (int(self.roiInitX) + int(self.centerX) + int(self.centerX) * 7.5 / 100))
            print("Faixa Vertical Inicio Y: %s" % (int(self.roi[1])))
            print("Faixa Vertical Fim Y: %s" % (int(self.roi[3])))

            # self.rangeVerticalInitX = int(self.centerX) - int(self.centerX) * 7.5 / 100
            

            # print("Largura: {}".format(self.roi[2]))
            # print("Altura: {}".format(self.roi[3]))
            # print("Centro Y:{}".format(self.centerY))
            # print("Centro X:{}".format(self.centerX))


            # print("Inicio Faixa Y:{}".format(self.minRangeY))
            # print("Fim Faixa Y:{}".format(self.maxRangeY))
            # print("Inicio Faixa X:{}".format(self.minRangeX))
            # print("Fim Faixa X:{}".format(self.maxRangeX))
            # print("Centro X:{}".format(self.centerX))
            # print("Altura %s" % (self.roi[3]))
            # print("Width %s" % (self.roi[2]))

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

            print("self.roiInitX {}", self.roiInitX)
            print("self.RoiEndX {}", self.roiEndX)
            
            print("self.RoiInitY {}", self.roiInitY)
            print("self.roiEndY {}", self.roiEndY)
            for c in contours:
                if cv2.contourArea(c) < 500:
                    continue
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print("cX {}", cX)
                print("cY {}", cY)  
                
                if (cY >= self.roiInitY and cY <= self.roiEndY and cX >= self.roiInitX and cX <= self.roiEndX):
                    cv2.circle(image_delimited, (cX, cY), 7, (255, 0, 0), -1)
                # if self.isCentro:
                   
                        # if (((cY >= self.rangeHorizontalInitY) and (cY <= self.rangeHorizontalEndY)) and ((cY >= self.rangeVerticalInitY) and (cY <= self.rangeVerticalEndY)) and ((cX >= self.rangeHorizontalInitX) and (cX <= self.rangeHorizontalEndX)) and ((cX >= self.rangeVerticalInitX) and (cX <= self.rangeVerticalEndX))):
                            
                        # cv2.circle(image_delimited, (cX, cY), 7, (255, 0, 0), -1)
                # else:
                #     if (((cY >= self.rangeHorizontalInitY) and (cY <= self.rangeHorizontalEndY)) and ((cY >= self.rangeVerticalInitY) and (cY <= self.rangeVerticalEndY)) and ((cX >= self.rangeHorizontalInitX) and (cX <= self.rangeHorizontalEndX)) and ((cX >= self.rangeVerticalInitX) and (cX <= self.rangeVerticalEndX))):
                #         cv2.circle(image_delimited, (cX, cY), 7, (255, 0, 0), -1)
                (x, y, w, h) = cv2.boundingRect(c)
                if h * w > 7600:
                    continue
                
                if self.minRangeY <= cY <= self.maxRangeY and self.minRangeX <= cX <= self.maxRangeX:
                    self.confirmCentro += 1
                    if self.confirmCentro == 3:
                        self.totalCruzamentos += 1

                        #CAPTURA A QUANTIDADE DE FRAMES DO VIDEO NESSE MOMENTO, SUBTRAI DA QUANTIDADE DE FRAMES QUE FOI STARTADO PELA ULTIMA VEZ EM ALGUM BRACO, E DIVIDE PELA 
                        #QTD DE FPS, E AO LOCALIZAR O BRACO QUE O RATO ESTAVA, ATRIBUI E SOMA NA VARIAVEL
                        if(self.confirmBaixo >= 2):
                            self.tempoTotalBaixo += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmEsquerda >= 3):
                             self.tempoTotalEsquerda += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmCima >= 3):
                            self.tempoTotalCima += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmDireita >= 3):
                            self.tempoTotalDireita += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado )  / self.video.get(cv2.CAP_PROP_FPS)
                        
                        timer = 0
                        if(timer == 0):
                            self.timerStartado = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                            timer = 1
                            
                        self.isCentro = True
                        self.isBaixo = False
                        self.isCima = False
                        self.isDireita = False
                        self.isEsquerda = False
                        self.confirmCima = 0
                        self.confirmDireita = 0
                        self.confirmEsquerda = 0
                        self.confirmBaixo = 0
                        # self.triggerTimer("centro")

                elif cY > self.centerY + 30 and self.minRangeX <= cX <= self.maxRangeX:
                    self.confirmBaixo += 1
                    if self.confirmBaixo == 2:
                        
                        #CAPTURA A QUANTIDADE DE FRAMES DO VIDEO NESSE MOMENTO, SUBTRAI DA QUANTIDADE DE FRAMES QUE FOI STARTADO PELA ULTIMA VEZ EM ALGUM BRACO, E DIVIDE PELA 
                        #QTD DE FPS, E AO LOCALIZAR O BRACO QUE O RATO ESTAVA, ATRIBUI E SOMA NA VARIAVEL
                        self.totalBracosAbertos += 1
                        if(self.confirmCentro >= 3):
                            self.tempoTotalCentro += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado )  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmEsquerda >= 3):
                             self.tempoTotalEsquerda += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado )  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmCima >= 3):
                            self.tempoTotalCima += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado )  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmDireita >= 3):
                            self.tempoTotalDireita += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado )  / self.video.get(cv2.CAP_PROP_FPS)
                            
                        timer = 0
                        if(timer == 0):
                            self.timerStartado = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                            timer = 1
                            
                        self.isBaixo = True
                        self.isCima = False
                        self.isDireita = False
                        self.isEsquerda = False
                        self.isCentro = False
                        self.confirmCima = 0
                        self.confirmDireita = 0
                        self.confirmEsquerda = 0
                        self.confirmCentro = 0
                        # print("Baixo")

                elif cY < self.centerY - 30 and self.minRangeX <= cX <= self.maxRangeX:
                    self.confirmCima += 1
                    if self.confirmCima == 3:
                        self.totalBracosAbertos += 1
                        
                        #CAPTURA A QUANTIDADE DE FRAMES DO VIDEO NESSE MOMENTO, SUBTRAI DA QUANTIDADE DE FRAMES QUE FOI STARTADO PELA ULTIMA VEZ EM ALGUM BRACO, E DIVIDE PELA 
                        #QTD DE FPS, E AO LOCALIZAR O BRACO QUE O RATO ESTAVA, ATRIBUI E SOMA NA VARIAVEL
                        if(self.confirmCentro >= 3):
                            self.tempoTotalCentro += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado )  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmEsquerda >= 3):
                             self.tempoTotalEsquerda += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado )  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmBaixo >= 2):
                            self.tempoTotalBaixo += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmDireita >= 3):
                            self.tempoTotalDireita += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        
                        timer = 0
                        if(timer == 0):
                            self.timerStartado = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                            timer = 1
                        self.isCima = True
                        self.isBaixo = False
                        self.isDireita = False
                        self.isEsquerda = False
                        self.isCentro = False
                        self.confirmBaixo = 0
                        self.confirmDireita = 0
                        self.confirmEsquerda = 0
                        self.confirmCentro = 0
                        # print("Cima")

                elif cX > self.centerX + 30 and self.minRangeY <= cY <= self.maxRangeY:
                    self.confirmDireita += 1
                    if self.confirmDireita == 3:
                        self.totalBracosFechados += 1
                        
                        #CAPTURA A QUANTIDADE DE FRAMES DO VIDEO NESSE MOMENTO, SUBTRAI DA QUANTIDADE DE FRAMES QUE FOI STARTADO PELA ULTIMA VEZ EM ALGUM BRACO, E DIVIDE PELA 
                        #QTD DE FPS, E AO LOCALIZAR O BRACO QUE O RATO ESTAVA, ATRIBUI E SOMA NA VARIAVEL
                        if(self.confirmCentro >= 3):
                            self.tempoTotalCentro += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmEsquerda >= 3):
                             self.tempoTotalEsquerda += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmBaixo >= 2):
                            self.tempoTotalBaixo += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)   / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmCima >= 3):
                            self.tempoTotalCima += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerStartado)   / self.video.get(cv2.CAP_PROP_FPS)
                        
                        timer = 0
                        if(timer == 0):
                            self.timerStartado = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                            timer = 1
                        self.isDireita = True
                        self.isBaixo = False
                        self.isCima = False
                        self.isEsquerda = False
                        self.isCentro = False
                        self.confirmCima = 0
                        self.confirmBaixo = 0
                        self.confirmEsquerda = 0
                        self.confirmCentro = 0
                        # print("Direita")
                
                elif cX < self.centerX - 30 and self.minRangeY <= cY <= self.maxRangeY:
                    self.confirmEsquerda += 1
                    if self.confirmEsquerda == 3:
                        self.totalBracosFechados += 1
                        
                        #CAPTURA A QUANTIDADE DE FRAMES DO VIDEO NESSE MOMENTO, SUBTRAI DA QUANTIDADE DE FRAMES QUE FOI STARTADO PELA ULTIMA VEZ EM ALGUM BRACO, E DIVIDE PELA 
                        #QTD DE FPS, E AO LOCALIZAR O BRACO QUE O RATO ESTAVA, ATRIBUI E SOMA NA VARIAVEL
                        if(self.confirmCentro >= 3): 
                            self.tempoTotalCentro += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES))  - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmEsquerda >= 3):
                             self.tempoTotalEsquerda += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES))  - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmBaixo >= 2):
                            self.tempoTotalBaixo += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES))  - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                        elif(self.confirmCima >= 3):
                            self.tempoTotalCima +=  (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerCima) / self.video.get(cv2.CAP_PROP_FPS)
                         
                        timer = 0
                        if(timer == 0):
                            self.timerStartado = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                            timer = 1   
                        self.isEsquerda = True
                        self.isBaixo = False
                        self.isCima = False
                        self.isDireita = False
                        self.confirmCima = 0
                        self.confirmBaixo = 0
                        self.confirmDireita = 0
                        self.confirmCentro = 0
                        # print("Esquerda")
                  
                cv2.rectangle(image_delimited, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                continue
            
            # SE A QUANTIDADE DE FRAMES ATUAL FOR IGUAL A QUANTIDADE DE FRAMES FINAL DO VIDEO, SETA O UTLIMO TIMER NA ULTIMA VARIAVEL
            # POR EXEMPLO, SE O RATO PAROU NO BRACO DE BAIXO POR ULTIMO, AO ENTRAR NESSA CONDICAO, ADICIONA O VALOR DO TIMER NA VARIAVEL DE BAIXO
            if(int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) == int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))):
                if(self.confirmCentro >= 3): 
                    self.tempoTotalCentro += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES))  - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                elif(self.confirmDireita >= 3):
                    self.tempoTotalEsquerda += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES))  - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                elif(self.confirmEsquerda >= 3):
                    self.tempoTotalEsquerda += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES))  - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                elif(self.confirmBaixo >= 2):
                    self.tempoTotalBaixo += (int(self.video.get(cv2.CAP_PROP_POS_FRAMES))  - self.timerStartado)  / self.video.get(cv2.CAP_PROP_FPS)
                elif(self.confirmCima >= 3):
                    self.tempoTotalCima +=  (int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - self.timerCima) / self.video.get(cv2.CAP_PROP_FPS)
            
            # PRINTAR OS VALORES NA TELA    
            cv2.putText(frame,'Timer Centro: ' +  str(round(self.tempoTotalCentro,2)), (35, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,255,0))
            cv2.putText(frame,'Timer Cima: ' +  str(round(self.tempoTotalCima,2)), (35, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,255,0))
            cv2.putText(frame,'Timer Direita: ' +  str(round(self.tempoTotalDireita,2)), (35, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,255,0))
            cv2.putText(frame,'Timer Baixo: ' +  str(round(self.tempoTotalBaixo,2)), (35, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,255,0))
            cv2.putText(frame,'Timer Esquerda: ' +  str(round(self.tempoTotalEsquerda,2)), (35, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,255,0))
            cv2.putText(frame,'Total Cruzamentos: ' +  str(round(self.totalCruzamentos,2)), (35, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,255,0))
            cv2.putText(frame,'Total Bracos Abertos: ' +  str(round(self.totalBracosAbertos,2)), (35, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,255,0))
            cv2.putText(frame,'Total Bracos Fechados: ' +  str(round(self.totalBracosFechados,2)), (35, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,255,0))
            # cv2.rectangle(frame, (self.roi[0], self.roi[1]), (self.roi[0] + self.roi[2], self.roi[1] + self.roi[3]), (200, 0, 0), 2)
            cv2.rectangle(frame, (int(self.rangeVerticalInitX), int(self.rangeVerticalInitY)), (int(self.rangeVerticalEndX), int(self.rangeVerticalEndY) + 15), (200, 0, 0), 2)
            cv2.rectangle(frame, (int(self.rangeHorizontalInitX), int(self.rangeHorizontalInitY)), (int(self.rangeHorizontalEndX), int(self.rangeHorizontalEndY) + 15), (200, 0, 0), 2)
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        
        else:
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
