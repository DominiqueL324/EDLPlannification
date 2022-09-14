from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import SignataireApi
from rest_framework.authtoken import views


urlpatterns = [
    path('viewset/', SignataireApi.as_view()),
]