from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.http import HttpResponse  
from django.views.generic import View, ListView
from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict


from dashboard.models import CrCompany, CrConfig, CrModelInfo, CrModelHistory
# from dashboard.controler import Company

import pandas as pd

# Create your views here.

class autocareinfo(View):  
    def get(self, request):
        model_history_list = CrModelHistory.objects.all()
        history_list = []
        
        for i in range(len(model_history_list)):
            count = i + 1
            company = model_history_list[i].company.company_name
            ip = model_history_list[i].company.company_ip
            temp_time = model_history_list[i].using_time
            using_time = temp_time.strftime("%d/%b/%Y %H:%M:%S")
            history_data = {
                                "count": count,
                                "company": company,
                                "ip": ip,
                                "using_time": using_time
                            }

            history_list.append(history_data)
            
        
        f = open('config/event.log', "r", encoding="UTF-8")   
        event_log = f.readlines()
        f.close()

        if len(event_log) > 20:
            event_log = event_log[-20:]


        context = {"page": "info", "history_list": history_list, "event_log": event_log}
        return render(request, 'dashboard/autoinfo.html', context)
    
    
class autocareconfig(View):  
    def get(self, request):
        config_data = CrConfig.objects.all()[0]
        model_list = CrModelInfo.objects.all()
        
        # https://velog.io/@jewon119/TIL00.-Django-ORM-%ED%95%84%EC%9A%94%ED%95%9C-column%EB%A7%8C-%EC%A7%80%EC%A0%95%ED%95%B4%EC%84%9C-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0
        model_id_list = model_list.values_list("model_id", flat=True)
        model_id_list = list(model_id_list)

        context = {"page": "config", "config_data": config_data, "model_list": model_list}
        response = render(request, 'dashboard/autoconfig.html', context)

        response.set_cookie(key='model_id_list', value=model_id_list)

        return response
    

class autocarecompany(View):  
    def get(self, request):

        company_models = CrCompany.objects.all()

        context = {"page": "company", "company_list" : company_models}
        return render(request, 'dashboard/autocompany.html', context)
    

