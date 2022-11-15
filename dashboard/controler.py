from django.shortcuts import render, redirect 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.http import HttpResponse  
from django.views.generic import View, ListView
from django.views.decorators.csrf import csrf_exempt

from dashboard.method import CompanyMethod, ConfigMethod, ModelMethod
from rest_framework.authtoken.models import Token

from dashboard.models import CrCompany, CrConfig, CrModelInfo, CrModelHistory

import secrets
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
import datetime

from .operator import get_schedule
from .autocare import autocare, logger
# from django.conf import settings

# http://www.iorchard.net/2016/07/11/curl_django_csrf_token_transmit.html
class company_control(APIView):
    # 토큰발행 https://uiandwe.tistory.com/1277
    # 토큰발행 user모델 확장 https://eunjin3786.tistory.com/253
    def company_set(request):
        company_name = request.POST["company_name"]
        company_ip = request.POST["company_ip"]
        company_operation = request.POST["company_operation"]

        company_token = secrets.token_hex(nbytes=16)

        print("controler")

        CompanyMethod.set(company_name,company_ip, company_token, company_operation)

        logger.create_company(company_name)
        
        return redirect('/autocare/company/')

    def company_search(request):
        company_name = request.POST["company_name"]
        company_models = CompanyMethod.get(company_name)

        context = {"page": "company", "company_list" : company_models}


        return render(request, 'dashboard/autocompany.html', context)


class config_control(APIView):
    def setting_save(request):
        model_id_list = request.COOKIES.get("model_id_list")
        learning_cycle = request.POST["learning_cycle"]
        learning_start = request.POST["learning_start"]

        model_id_list = eval(model_id_list)

        model_path_list = request.POST.getlist("model_path")
        model_api_list = request.POST.getlist("model_api")

        
        ConfigMethod.set(learning_cycle = learning_cycle, learning_start = learning_start)
        for i in range(len(model_id_list)):
            model_id = int(model_id_list[i])
            model_path = model_path_list[i]
            model_api = model_api_list[i]

            temp = model_path.split('/')[-1]
            model_path = model_path.replace(temp,"")

            ModelMethod.set(model_id, model_path = model_path, model_api = model_api)

        logger.update_config()

        return redirect('/autocare/config/')

    def collection_set(request, collection_oper):
        ConfigMethod.set(collection_oper = collection_oper)
        logger.update_collection(collection_oper)
        return redirect('/autocare/config/')
    
    def labeling_set(request, labeling_oper):
        ConfigMethod.set(labeling_oper = labeling_oper)
        logger.update_labeling(labeling_oper)
        return redirect('/autocare/config/')

    def learning_set(request, learning_oper):
        now = datetime.datetime.now()
        ConfigMethod.set(learning_oper = learning_oper, start_date=now)
        logger.update_learning(learning_oper)
        get_schedule(learning_oper)

        
        return redirect('/autocare/config/')


class info_control(APIView):
    def do_learning(request):
        autocare.learning(1, 0)
        autocare.learning(2, 0)
        return redirect('/autocare/info/')

