from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import EdlApi
from rest_framework.authtoken import views


urlpatterns = [
    path('viewset/', EdlApi.as_view()),
]