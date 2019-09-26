from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic, View
from .tracker import Tracker

class TestSetup:
    __instance = None
    animal = ""
    videoPath = None
    dateTime = ""
    initialX = 0
    initialY = 0
    width = 0
    height = 0
    roi = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if TestSetup.__instance == None:
           TestSetup()
        return TestSetup.__instance

    def __init__(self):
<<<<<<< HEAD
        self.video = cv2.VideoCapture(r"C:\Users\edure\labcruz_backend\mouse_tracker\video.mp4")
=======
        """ Virtually private constructor. """
        if TestSetup.__instance != None:
           raise Exception("This class is a singleton!")
        else:
           TestSetup.__instance = self
>>>>>>> 934b337fe792251e07cced7aa44fdfb0fa419bc8

class MazeAreaDimension():
    initX = 0
    initY = 0
    areaW = 0
    areaH = 0

mazeSelectedArea = MazeAreaDimension()

test_setup = TestSetup()

class Analysis(View):
    def __init__(self):
        self.tracker = tracker

    def getROIArea(request):
        mazeSelectedArea.initX = request.POST.get('initX')
        mazeSelectedArea.initY = request.POST.get('initY')
        mazeSelectedArea.areaW = request.POST.get('areaWidth')
        mazeSelectedArea.areaH = request.POST.get('areaHeight')
        roi_array = []
        roi_array.append(int(mazeSelectedArea.initX))
        roi_array.append(int(mazeSelectedArea.initY))
        roi_array.append(int(mazeSelectedArea.areaW))
        roi_array.append(int(mazeSelectedArea.areaH))
        TestSetup.getInstance.roi = roi_array
        print("TestSetup videoPath %s" % (TestSetup.getInstance.videoPath))
        print("TestSetup roi %s" % (TestSetup.getInstance.roi))

        print("ROIIIII area: Initial X: %s, Initial Y: %s, Width: %s, Height: %s" % (mazeSelectedArea.initX, mazeSelectedArea.initY, mazeSelectedArea.areaW, mazeSelectedArea.areaH))
        data = {}
        return JsonResponse({})
        # return render(request, 'mouse_tracker/index.html', {})

    def streamImage(request):
        try:
            if TestSetup.getInstance.videoPath is not None and TestSetup.getInstance.videoPath is not 0:
                print(" Entrou no primeiro IF")
                if TestSetup.getInstance.roi == 0:
                    print("Roi é nulo")
                    return StreamingHttpResponse(getFirstFrame(Tracker(TestSetup.getInstance.videoPath, TestSetup.getInstance.roi)), content_type="multipart/x-mixed-replace;boundary=frame")
                else:
                    print("Roi nao é nulo")
                    return StreamingHttpResponse(generateFrames(Tracker(TestSetup.getInstance.videoPath, TestSetup.getInstance.roi)),content_type="multipart/x-mixed-replace;boundary=frame")
            else:
                print("Rendering image from Camera IP")
                return StreamingHttpResponse(generateFrames(Tracker(TestSetup.getInstance.videoPath, TestSetup.getInstance.roi)),content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            pass

    def startTest(request):
        print(TestSetup.getInstance.roi)
        return render(request, 'mouse_tracker/index.html', {})


#Métodos relacionados a Câmera IP
class CameraIPAnalysis(Analysis):

    def renderWithoutAnalysis(request):
        TestSetup.getInstance.roi = None
        TestSetup.getInstance.videoPath = 0
        # startAnalysis = False
        context = {}
        return render(request, 'mouse_tracker/index.html', context)

    
#Métodos relacionados a um Vídeo Escolhido
class VideoFileAnalysis(Analysis):

    def get_filepath(request):
        print("Chamando get_filepath")
        if request.method == "POST":
            print("Entrou no metodo POST")
            print(str(request.POST.get('filepath_value')))
            TestSetup.getInstance.videoPath = str(request.POST.get('filepath_value'))
            TestSetup.getInstance.roi = 0
            return render(request, 'mouse_tracker/index.html', {})
        return JsonResponse({})

    def renderWithoutAnalysis(request):
        TestSetup.getInstance.roi = None
        context = {}
        return render(request, 'mouse_tracker/index.html', context)


    
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

def home(request):
    return render(request, 'mouse_tracker/home.html', {})


