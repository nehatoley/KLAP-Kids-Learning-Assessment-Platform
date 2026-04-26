from django.urls import path
from .views import camera_page, detect_api

urlpatterns = [
    path('camera/', camera_page, name='camera'),
    path('api/', detect_api, name='detect_api'),
]