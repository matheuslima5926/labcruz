from django.urls import path

from . import views

urlpatterns = [
    path('livefe', views.livefe, name='livefe'),
    path('', views.stream, name='stream'),
]