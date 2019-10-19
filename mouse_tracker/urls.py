from django.urls import path
from .views import CameraIPAnalysis, VideoFileAnalysis, Analysis, Records
from .tracker import Tracker
from . import views

urlpatterns = [
    #Rota para decidir se o video analisado será da Camera ou de um Arquivo
    path('', views.home, name='home'),

    #Rota para capturar area selecionada
    path('getROI', Analysis.getROIArea, name='getROI'),
    path('start_test', Analysis.startTest, name="start_test"),

    #Rota que faz o stream do Teste
    path('stream_image', Analysis.streamImage, name="stream_image"),

    # Ao escolher Camera IP como fonte do video 
    # essas rotas serão chamadas
    path('renderWA', CameraIPAnalysis.renderWithoutAnalysis, name='renderWA'),

    path('timer', Tracker.triggerTimer, name='timer'),

    # Ao escolher Vide File como fonte do vídeo
    # essas rotas serão chamadas
    path('renderVWA', VideoFileAnalysis.renderWithoutAnalysis, name='renderVWA'),
    path('get_filepath', VideoFileAnalysis.get_filepath, name='get_filepath'),

    path('registro', Records.get_animals, name="records"),
    path('saveAnimal', Records.create_animal, name="saveAnimal"),
    path('deleteAnimal', Records.delete_animal, name="deleteAnimal"),
    path('updateAnimal', Records.update_animal, name="updateAnimal"),
    path('animais', Records.get_animals, name='animais'),
    path('historico', Records.get_tests, name='historico')
    
]
