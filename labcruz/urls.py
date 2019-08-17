from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('mouse_tracker.urls')),
    path('admin/', admin.site.urls),
]
