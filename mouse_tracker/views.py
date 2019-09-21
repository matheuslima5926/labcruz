from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from .tracker import Tracker

class MazeAreaDimension():
    initX = 0
    initY = 0
    areaW = 0
    areaH = 0

videoSource = "camera"
startAnalysis = False
filePath = ""

mazeSelectedArea = MazeAreaDimension()

class Analysis(object):
    def __init__(self, tracker):
        self.tracker = tracker


    def getROIArea(request):
        mazeSelectedArea.initX = request.POST.get('initX')
        mazeSelectedArea.initY = request.POST.get('initY')
        mazeSelectedArea.areaW = request.POST.get('areaWidth')
        mazeSelectedArea.areaH = request.POST.get('areaHeight')
        print("ROI area: Initial X: %s, Initial Y: %s, Width: %s, Height: %s" % (mazeSelectedArea.initX, mazeSelectedArea.initY, mazeSelectedArea.areaW, mazeSelectedArea.areaH))
        data = {}
        return JsonResponse(data)

    def generateFrames(tracker):
        if tracker:
            print("Chegou em generateFrames")
        try:
            while True:
                frame = tracker.get_frame()
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + 
                b'\r\n\r\n')
        except:
            return

    def streamCameraPlain(request):
        return
    def analise(request):
        try:
            print("Streaming Analise!")
            return StreamingHttpResponse(generateFrames(Tracker(True)),content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            pass

#Métodos relacionados a Câmera IP
class CameraIPAnalysis(Analysis):

    videoSource = 'camera'
    #tracker = Tracker(True)

    def streamAnalysis(tracker):
        try:
            while True:
                frame = tracker.get_frame()
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + 
                b'\r\n\r\n')
        except:
            return

    def streamWithAnalsysis(request):
        startAnalysis = True
        context = {
            'startAnalysis': startAnalysis,
            'videoSource': videoSource
        }
        return render(request, 'mouse_tracker/index.html', context)

    def streamWithoutAnalysis(request, ):
        tracker = Tracker(True)
        an = Analysis(tracker)
        startAnalysis = False
        context = {
            'startAnalysis': startAnalysis,
            'videoSource': videoSource
        }
        return render(request, 'mouse_tracker/index.html', context)

    
#Métodos relacionados a um Vídeo Escolhido
class VideoFileAnalysis(Analysis):
    filePath = ""
    tracker = Tracker(False, filePath)
    def showFirstFrames(tracker):
        try:
            for f in range(1,2):
                frame = tracker.get_frame()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + 
                    b'\r\n\r\n')
        except:
            return

    def streamAnalysis(tracker):
        try:
            while True:
                frame = tracker.get_frame()
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + 
                b'\r\n\r\n')
        except:
            return
    


def getFirstFrame(cam):
    try:
        for f in range(1,2):
            frame = cam.get_frame()
            print("Chegou Aqui!")
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + 
                b'\r\n\r\n')
    except:
        return


def generateFrames(tracker):
    try:
        while True:
            frame = tracker.get_frame()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + 
            b'\r\n\r\n')
    except:
        return

#Vai fazer o stream da imagem capturada pela camera IP
def livefe(request):
    try:
        #Video é LIVE, imagem da câmera IP será processada
        tracker = Tracker(True)
        return StreamingHttpResponse(generateFrames(tracker),content_type="multipart/x-mixed-replace;boundary=frame")
    except:  
        pass

#Fará analise de um video escolhido
def analyseAndStream(request):
    print("File path selecionado: %s" % (filePath))
    try:
        tracker = Tracker(False, filePath)
        return StreamingHttpResponse(generateFrames(tracker),content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def stream(request):
    print(request.method)
    if request.method == "GET":
        print("Start analysis should be false!")
        startAnalysis = False
    else:
        print("Start analysis should be true!")
        startAnalysis = True
    context = {
        'startAnalysis': startAnalysis,
        'videoSource': videoSource
    }
    # return render(request, 'mouse_tracker/index.html', context)
    return render(request, 'mouse_tracker/index.html', context)

def get_area_selected(request):

    mazeSelectedArea.initX = request.POST.get('initX')
    mazeSelectedArea.initY = request.POST.get('initY')
    mazeSelectedArea.areaW = request.POST.get('areaWidth')
    mazeSelectedArea.areaH = request.POST.get('areaHeight')
    print("ROI area: Initial X: %s, Initial Y: %s, Width: %s, Height: %s" % (mazeSelectedArea.initX, mazeSelectedArea.initY, mazeSelectedArea.areaW, mazeSelectedArea.areaH))
    data = {}
    return JsonResponse(data)

def home(request):
    return render(request, 'mouse_tracker/home.html', {})

def get_filepath(request):
    if request.method == "POST":
        filePath = request.POST.get('filepath_value')
        print("File path %s" % (filePath))
        startAnalysis = False
        context = {
            'startAnalysis': startAnalysis,
            'videoSource': 'file'
        }
        return render(request, 'mouse_tracker/index.html', {})
    return JsonResponse({})

