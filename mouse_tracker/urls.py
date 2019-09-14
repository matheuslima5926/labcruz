from django.urls import path

from . import views

urlpatterns = [
    path('livefe', views.livefe, name='livefe'),
    path('', views.stream, name='stream'),
    path('get_area', views.get_area_selected, name='get_area_selected'),
]
