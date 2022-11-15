from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .ecgmodule import CAmodel, HFmodel
import datetime
import json
import os
from dashboard.method import ConfigMethod
# from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@api_view(['GET'])
def TestAPI(request):
    #Test
    #Test2
    return Response("GAILAB Test API server")

class CAAPI(APIView):
    # @csrf_exempt
    def get(self, request):
        user_id = request.data.get("user_id")
        user_data = request.data.get("user_data")
        exercise_id = request.data.get("exercise_id")
        exercise_serial = request.data.get("exercise_serial")

        controler = CAmodel()
        prob, result_prob, result = controler.get_result(user_data)

        config_data = ConfigMethod.get()
        if config_data.collection_oper=='Y':
            path = "AIAPI/data/raw_data/"
            data_collection(user_id,"arrhythmia",prob,result,user_data, path)
        if config_data.labeling_oper=='Y':
            path = "AIAPI/data/label_data/"
            if result_prob==0:
                data_labeling("normal",prob,user_data,path)
            else:
                data_labeling("arrhythmia",prob,user_data,path)     

        data = {"user_id": user_id, 
                "probability": prob, 
                "class_num": result_prob, 
                "class": result,
                "exercise_id": exercise_id,
                "exercise_serial": exercise_serial}
        return Response(data, status=200)#테스트용 Response

    def post(self, request):
        user_id = request.data.get("user_id")
        user_data = request.data.get("user_data")
        exercise_id = request.data.get("exercise_id")
        exercise_serial = request.data.get("exercise_serial")
        
        controler = CAmodel()
        prob, result_prob, result = controler.get_result(user_data)
        
        config_data = ConfigMethod.get()
        if config_data.collection_oper=='Y':
            path = "AIAPI/data/raw_data/"
            data_collection(user_id,"arrhythmia",prob,result,user_data, path)
        if config_data.labeling_oper=='Y':
            path = "AIAPI/data/label_data/"
            if result_prob==0:
                data_labeling("normal",prob,user_data,path)
            else:
                data_labeling("arrhythmia",prob,user_data,path)
        

        data = {"user_id": user_id, 
                "probability": prob, 
                "class_num": result_prob, 
                "class": result,
                "exercise_id": exercise_id,
                "exercise_serial": exercise_serial}
        return Response(data, status=200)#테스트용 Response

class HFAPI(APIView):
    # @csrf_exempt
    def get(self, request):
        user_id = request.data.get("user_id")
        user_data = request.data.get("user_data")
        exercise_id = request.data.get("exercise_id")
        exercise_serial = request.data.get("exercise_serial")

        controler = HFmodel()
        prob, result_prob, result = controler.get_result(user_data)

        config_data = ConfigMethod.get()
        if config_data.collection_oper=='Y':
            path = "AIAPI/data/raw_data/"
            data_collection(user_id,"heart_failure",prob,result,user_data, path)
        if config_data.labeling_oper=='Y':
            path = "AIAPI/data/label_data/"
            if result_prob==0:
                data_labeling("normal",prob,user_data,path)
            else:
                data_labeling("heart_failure",prob,user_data,path)

        data = {"user_id": user_id, 
                "probability": prob, 
                "class_num": result_prob, 
                "class": result,
                "exercise_id": exercise_id,
                "exercise_serial": exercise_serial}
        return Response(data, status=200)#테스트용 Response
    
    def post(self, request):
        # path = "AIAPI/data/raw_data/HF/"
        user_id = request.data.get("user_id")
        user_data = request.data.get("user_data")
        exercise_id = request.data.get("exercise_id")
        exercise_serial = request.data.get("exercise_serial")

        controler = HFmodel()
        prob, result_prob, result = controler.get_result(user_data)

        config_data = ConfigMethod.get()
        if config_data.collection_oper=='Y':
            path = "AIAPI/data/raw_data/"
            data_collection(user_id,"심부전",prob,result,user_data, path)
        if config_data.labeling_oper=='Y':
            path = "AIAPI/data/label_data/"
            if result_prob==0:
                data_labeling("normal",prob,user_data,path)
            else:
                data_labeling("heart_failure",prob,user_data,path)

        data = {"user_id": user_id, 
                "probability": prob, 
                "class_num": result_prob, 
                "class": result,
                "exercise_id": exercise_id,
                "exercise_serial": exercise_serial}

        return Response(data, status=200)#테스트용 Response

# @csrf_exempt
class UserView(APIView):
    # @csrf_exempt
    def get(self, request):
        print("GET")
        return Response("ok", status=200)#테스트용 Response
    

def data_collection(user_id, disease, prob, result, user_data, path):
    now = datetime.datetime.now()
    format = '%Y%m%d%H%M%S%Z'
    file_name = datetime.datetime.strftime(now,format)
    file_path = path + file_name + ".json"

    save_data = {"user_id": user_id, 
                "disease" : disease,
                "probability": prob, 
                "class": result,
                "data": user_data}

    with open(file_path, 'w', encoding='UTF-8-sig') as f:
        json.dump(save_data, f,  ensure_ascii=False) 
    
    f.close()

    return

def data_labeling(result, prob, user_data, path):
    now = datetime.datetime.now()
    format = '%Y%m%d%H%M%S%Z'
    file_name = datetime.datetime.strftime(now,format)
    file_path = path + result + "_" +file_name + ".json"

    save_data = {"class": result,   
                "probability": prob, 
                "data": user_data}

    with open(file_path, 'w', encoding='UTF-8-sig') as f:
        json.dump(save_data, f,  ensure_ascii=False) 
    
    f.close()

    return