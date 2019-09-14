from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from .tracker import VideoCapture

class MazeAreaDimension():
    initX = 0
    initY = 0
    areaW = 0
    areaH = 0

mazeSelectedArea = MazeAreaDimension()
cam = VideoCapture()

def gen(cam):
    try:
        while True:
            frame = cam.get_frame()
        
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + 
            b'\r\n\r\n')
    except:
        return

def livefe(request):
    try:
        return StreamingHttpResponse(gen(VideoCapture()),content_type="multipart/x-mixed-replace;boundary=frame")
    except:  
        pass

def stream(request):
    context = {
        'something': "something"
    }
    return render(request, 'mouse_tracker/index.html', context)

def get_area_selected(request):

    mazeSelectedArea.initX = request.POST.get('initX')
    mazeSelectedArea.initY = request.POST.get('initY')
    mazeSelectedArea.areaW = request.POST.get('areaWidth')
    mazeSelectedArea.areaH = request.POST.get('areaHeight')

    print("ROI area: Initial X: %s, Initial Y: %s, Width: %s, Height: %s" % (mazeSelectedArea.initX, mazeSelectedArea.initY, mazeSelectedArea.areaW, mazeSelectedArea.areaH))
    data = {}
    return JsonResponse(data)



