from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import LogementApi
from rest_framework.authtoken import views


urlpatterns = [
    path('viewset/', LogementApi.as_view()),
]