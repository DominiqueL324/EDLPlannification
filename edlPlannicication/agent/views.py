from django.shortcuts import render
from edlPlannicication.views import config, authe,database
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import date, datetime,time,timedelta
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

# Create your views here.

class AgentApi(APIView):

    def post(self,request):
        data = request.data
        #database.child('agent_secteur').child(data.auto_key).set(data)
        #juste pour test avec clef autogénérée plus tard ce sera avec set pour des clef manuelement definie
        agent = {} 
        try:
            agent = database.child('agent_secteur').push(data)
            database.child('signataire').child(agent['name']).set(data)
        except:
            return JsonResponse({"status":0},status=500)
        return Response(agent['name'],status=status.HTTP_201_CREATED)

    def put(self,request):
        data = request.data
        #database.child('agent_secteur').child(data.auto_key).set(data)
        #juste pour test avec clef autogénérée plus tard ce sera avec set pour des clef manuelement definie
        agent = {} 
        try:        
            agent = database.child('agent_secteur').child(data['id']).update(data)
            database.child('signataire').child(data['id']).update(data)
        except:
            return JsonResponse({"status":0},status=500)
        return Response(agent,status=status.HTTP_200_OK)

    def delete(self,request):
        data = request.data
        #database.child('agent_secteur').child(data.auto_key).set(data)
        #juste pour test avec clef autogénérée plus tard ce sera avec set pour des clef manuelement definie
        agent = {} 
        try:
            agent = database.child('agent_secteur').child(data['id']).remove()
        except:
            return JsonResponse({"status":0},status=500)
        return Response({},status=status.HTTP_200_OK)



