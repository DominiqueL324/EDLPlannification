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

class EdlApi(APIView):

    def get(self,request):

        final_=[]
        parts_ = []
        if request.GET.get('id',None) is not None:
            #recupération de l'EDL By id
            edl = database.child("edl").child(request.GET.get('id')).get()
            fin_ = edl.val()
            #Verficiation de réponse
            if fin_ is not None:
                fin_['id'] = request.GET.get('id')
                #recupération des participants
                participants_edl = database.child("participants_edl").order_by_child("edl").equal_to(request.GET.get('id')).get()
                chk  = participants_edl.val()
                if chk is not None:
                    #recupération de chaque signataire correspondant à un participant
                    for participant in participants_edl.each():
                        gar = database.child('signataire').child(participant.val()["participant"]).get().val()
                        parts_.append(gar)
                    fin_['participants'] = parts_
                    fin_['agent_secteur'] = database.child('agent_secteur').child(fin_['agent_secteur']).get().val()
                    fin_['logement'] = database.child('logement').child(fin_['logement']).get().val()

                return JsonResponse(fin_,status=200)
            return JsonResponse({},status=200)

        edl = database.child("edl").get()
        for ed in edl.each():
            ed.val()['id'] = ed.key()
            ed.val()['agent_secteur'] = database.child('agent_secteur').child(ed.val()['agent_secteur']).get().val()
            ed.val()['logement'] = database.child('logement').child(ed.val()['logement']).get().val()
            #recupération des participants de l'EDL en question
            participants_edl = database.child("participants_edl").order_by_child("edl").equal_to(ed.key()).get()
            #Ajout de chaque particpant dans un tableau de participants
            for participant in participants_edl.each():
                gar = database.child('signataire').child(participant.val()["participant"]).get().val()
                parts_.append(gar)
            #ajout du tableau de participants dans l'EDL
            ed.val()['participants'] = parts_
            #ajout de l'EDL dans le tableau final
            final_.append(ed.val())
        return JsonResponse({"edl":final_},status=200)
        
        

    def post(self,request):
        #database.child('agent_secteur').child(data.id).set(data)
        #juste pour test avec clef autogénérée plus tard ce sera avec set pour des clef manuelement definie
        parts_ = []
        final_ = []
        data = request.data
        edl = {
            "ref_edl":data['ref_edl'],
            "date_":data['date_'],
            "type_edl":data['type_edl'].lower(),
            "motif_depart":data['motif_depart'].lower(),
            "avancement":data['avancement'].lower(),
            "logement":data['logement'],
            "rdv":data['rdv'],
            "agent_secteur":data['agent_secteur'],           
        } 
    
        try:
            edl = database.child('edl').push(edl)
            for participant in data['participants']:
                participants_edl={
                    "participant":participant['id'],
                    "edl":edl['name'],                  
                }
                database.child('participants_edl').push(participants_edl)
                parts_.append( database.child('signataire').child(participant["id"]).get().val() )
            edl = database.child("edl").child(edl['name']).get()
            final_ = edl.val()
            final_['id']=edl['name']
            final_['participants'] = parts_
            final_['agent_secteur'] = database.child('agent_secteur').child(data['agent_secteur']).get().val()
            final_['logement'] = database.child('logement').child(data['logement']).get().val()
        except:
            return JsonResponse({"status":0},status=500)
        return Response(final_,status=status.HTTP_200_OK)
    
    def put(self,request):
        data = request.data
        parts_ = []
        final_ = []
        edl = {
            "ref_edl":data['ref_edl'].lower(),
            "date_":data['date_'],
            "type_edl":data['type_edl'].lower(),
            "motif_depart":data['motif_depart'].lower(),
            "avancement":data['avancement'].lower(),
            "logement":data['logement'],
            "rdv":data['rdv'],
            "agent_secteur":data['agent_secteur'],          
        } 

        try:
            #mise à jour de l'EDL
            edl = database.child('edl').child(data['id']).update(edl)

            #suppression des anciens participants
            old_part = database.child('participants_edl').order_by_child("edl").equal_to(data['id']).get()
            for old in old_part.each():
                database.child("participants_edl").child(old.key()).remove()

            #fin de suppression ajout de la nouvelle liste de participant pour l'EDL
            
            for participant in data["participants"]:
                participants_edl={
                    "participant":participant['id'],
                    "edl":data['id'],                  
                }
                database.child('participants_edl').push(participants_edl)
                parts_.append( database.child('signataire').child(participant["id"]).get().val() )
            edl = database.child("edl").child(data['id']).get()
            final_ = edl.val()
            final_['id']=data['id']
            final_['participants'] = parts_
            final_['agent_secteur'] = database.child('agent_secteur').child(data['agent_secteur']).get().val()
            final_['logement'] = database.child('logement').child(data['logement']).get().val()

        except:
            return JsonResponse({"status":0},status=500)
        return Response(final_,status=status.HTTP_201_CREATED)

    def delete(self,request):
        data = request.data
        try:
            database.child("participants_edl").order_by_child("edl").equal_to(data["id"]).remove()
            database.child("edl").child(data["id"]).remove()
        except:
            return JsonResponse({"status":0},status=500)
        return Response({},status=status.HTTP_200_OK)







