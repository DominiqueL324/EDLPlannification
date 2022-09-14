from django.shortcuts import render
import pyrebase
 
config={
    "apiKey": "AIzaSyCmvy45SEkwQk1AauHKurx4_vWQ_ziT3_w",
    "authDomain": "plannificationedl-217b8.firebaseapp.com",
    "databaseURL": "https://plannificationedl-217b8-default-rtdb.firebaseio.com/",
    "projectId": "plannificationedl-217b8",
    "storageBucket": "plannificationedl-217b8.appspot.com",
    "messagingSenderId": "734440369139",
    "appId": "1:734440369139:web:d859663935a5bbe5af0086",
    "measurementId": "G-H67NDY9EX3"
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()