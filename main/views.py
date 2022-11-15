from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.http import HttpResponse  
from django.views.generic import View
from django.contrib.auth.views import LoginView

from django.contrib.auth import login as auth_login

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class login(LoginView):  
    def GET(self, request):
        print("Login page")
        return render(request, 'main/main.html')

    def POST(self, request):
        print("Login page")
        

        return render(request, 'main/main.html')
