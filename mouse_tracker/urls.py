from django.urls import path
from .views import CameraIPAnalysis, VideoFileAnalysis, Analysis
from . import views

urlpatterns = [
    #Rota para decidir se o video analisado será da Camera ou de um Arquivo
    path('', views.home, name='home'),
    #Rota para capturar area selecionada
    path('getROI', Analysis.getROIArea, name='getROI'),

    # Ao escolher Camera IP como fonte do video 
    # essas rotas serão chamadas
    path('streamWA', CameraIPAnalysis.streamWithoutAnalysis, name='streamWA'),
    path('streamA', CameraIPAnalysis.streamWithAnalsysis, name='streamA'),

    # Ao escolher Vide File como fonte do vídeo
    # essas rotas serão chamadas


    path('analise', Analysis.analise, name='analise'),

    path('livefe', views.livefe, name='livefe'),
    path('stream', views.stream, name='stream'),
    path('analysis', views.analyseAndStream, name='analysis'),
    path('get_area', views.get_area_selected, name='get_area_selected'),
    path('get_filepath', views.get_filepath, name='get_filepath'),
]
