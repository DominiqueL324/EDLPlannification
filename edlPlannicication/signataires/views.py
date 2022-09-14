from ast import Delete
from email.policy import HTTP
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

class SignataireApi(APIView):

    def get(self,request):

        final_=[]
        if request.GET.get('role',None) is not None:
            signataires_=[]
            signataires = database.child("signataire").order_by_child('role').equal_to(request.GET.get('role')).get()
            for signe in signataires.each():
                signe.val()['id'] = signe.key()
                signataires_.append(signe.val())
            return JsonResponse({"signataires":signataires_},status=200)
        
        if request.GET.get('id',None) is not None:
            signataires = database.child("signataire").child(request.GET.get('id')).get()
            fin_ = signataires.val()
            if fin_ is not None:
                fin_['id'] = request.GET.get('id')
                return JsonResponse(fin_,status=200)
            return JsonResponse({},status=200)

        signataires = database.child("signataire").get()
        for signe in signataires.each():
            signe.val()['id'] = signe.key()
            final_.append(signe.val())
        return JsonResponse({"signataires":final_},status=200)
        
        

    def post(self,request):
        data = request.data
        locat = database.child("signataire").order_by_child("email").equal_to(data['email'].lower()).get().val()
        if type(locat) != list :
            return Response({"status":"existing email"},status=status.HTTP_409_CONFLICT)
        #database.child('agent_secteur').child(data.id).set(data)
        #juste pour test avec clef autogénérée plus tard ce sera avec set pour des clef manuelement definie
        signataire = {
            "nom":request.POST.get("nom",None).lower(),
            "prenom":request.POST.get("prenom",None).lower(),
            "email":request.POST.get("email",None).lower(),
            "fixe":request.POST.get("fix_phone",None).lower(),
            "mobile":request.POST.get("mobile_phone",None).lower(),
            "role":request.POST.get("role",None).lower(),
            "reference":request.POST.get("reference",None),
            "numero_voie":request.POST.get("numero_voie",None),
            "extension_voie":request.POST.get("extension_voie",None),
            "type_voie":request.POST.get("type_voie",None),
            "code_postal":request.POST.get("code_postal",None),
            "ville":request.POST.get("ville",None),
            "complement_adresse":request.POST.get("complement_adresse",None), 
            "compte_client":request.POST.get("compte_client",None)           
        } 
    
        try:
            signataire = database.child('signataire').push(signataire)
            #database.child('signataire').child(data.id).set(signataire)
            if request.POST.get("bank",None) is not None:
                for bk in request.POST.get("bank",None):
                    banque={
                        "compte":bk['compte'],
                        "banque":bk['banque'],
                        "bic":bk["bic"],
                        "iban":bk["iban"],
                        "signataire":signataire['name']                  
                    }
                    signataire = database.child('compte_bancaire').push(banque)
                    #database.child('compte_bancaire').child(data.id).set(banque)
        except:
            return JsonResponse({"status":0},status=500)
        return Response(signataire,status=status.HTTP_201_CREATED)
    
    def put(self,request):
        data = request.data
        locat = database.child("signataire").order_by_child("email").equal_to(data['email'].lower()).get().val()
        if type(locat) != list :
            locat1 = database.child("signataire").order_by_child("email").equal_to(data['email'].lower()).get()
            if locat1[0].key() != data["id"]:
                return Response({"stat":locat1[0].key()},status=status.HTTP_409_CONFLICT)

        signataire = {
            "nom":request.POST.get("nom",None),
            "prenom":request.POST.get("prenom",None),
            "email":request.POST.get("email",None),
            "fixe":request.POST.get("fix_phone",None),
            "mobile":request.POST.get("mobile_phone",None),
            "role":request.POST.get("role",None),
            "reference":request.POST.get("reference",None),
            "numero_voie":request.POST.get("numero_voie",None),
            "extension_voie":request.POST.get("extension_voie",None),
            "type_voie":request.POST.get("type_voie",None),
            "code_postal":request.POST.get("code_postal",None),
            "ville":request.POST.get("ville",None),
            "complement_adresse":request.POST.get("complement_adresse",None), 
            "compte_client":request.POST.get("compte_client",None)           
        } 

        try:
            signataire = database.child('signataire').child(request.POST.get("id",None)).update(signataire)
            if request.POST.get("bank",None) is not None:
                for bk in request.POST.get("bank",None):
                    banque={
                        "compte":bk['compte'],
                        "banque":bk['banque'],
                        "bic":bk["bic"],
                        "iban":bk["iban"],
                        "signataire":signataire['name']                  
                    }
                    signataire = database.child('compte_bancaire').child(bk['id']).update(banque)
        except:
            return JsonResponse({"status":0},status=500)
        return Response(signataire,status=status.HTTP_201_CREATED)

    def delete(self,request):
        data = request.data
        try:
            database.child("signataire").child(data["id"]).remove()
        except:
            return JsonResponse({"status":0},status=500)
        return Response({},status=status.HTTP_200_OK)







