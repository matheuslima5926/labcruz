from django.urls import path

from . import views

urlpatterns = [
    path('', views.livefe, name='livefe'),
    # path('stream', views.stream, name='stream'),
]