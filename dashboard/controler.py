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
        ConfigMethod.set(learning_oper = learning_oper)
        logger.update_learning(learning_oper)
        return redirect('/autocare/config/')


class info_control(APIView):
    def do_learning(request):
        autocare.learning(1, 0)
        autocare.learning(2, 0)
        return redirect('/autocare/info/')

class autocare():
    def learning(model_id, case):
        # case - 0: 자동학습 1: 강제학습
        model_data = ModelMethod.get(model_id)
        model_name = model_data.model_name
        model_path = model_data.model_path
        model_file = model_path + model_data.model_file
        model = tf.keras.models.load_model(model_file)
        dataset = pd.read_csv(model_data.data_path)

        x_data = dataset.iloc[:,:-1]
        y_data = dataset.iloc[:,-1]

        x_data = np.array(x_data)
        y_data = np.array(y_data)

        x_data = x_data.reshape(-1,125,1)
        y_data = tf.keras.utils.to_categorical(y_data,2)

        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.8, random_state=1, shuffle=True)

        model.fit(x_train,y_train,epochs=1,batch_size=128, validation_data=(x_test, y_test))

        now = datetime.datetime.now()
        format = '%Y%m%d%H%M%S%Z'
        file_date = datetime.datetime.strftime(now,format)

        new_rname =  model_data.model_rname + '_' + file_date + '.h5'

        print(new_rname)

        ModelMethod.set(model_id=model_id,model_file=new_rname)

        model.save(model_path + new_rname)
        if case == 0:
            logger.update_model(model_name)
        else:
            logger.auto_update_model(model_name)


        return

class logger():
    def update_model(model_name):
        logging_time = logger.get_time()
        log = logging_time + model_name + " 모델 업데이트 진행"
        logger.set_log(log)
        return 

    def auto_update_model(model_name):
        logging_time = logger.get_time()
        log = logging_time + model_name + " 모델 자동 업데이트"
        logger.set_log(log)
        return 
    
    def create_company(company_name):
        logging_time = logger.get_time()
        log = logging_time + company_name + " 신규 업체 등록"
        logger.set_log(log)
        return 
    
    def update_collection(case):
        # case N: 미수집 Y: 수집
        logging_time = logger.get_time()
        if case == 'N':
            log = logging_time + "데이터 자동 수집 종료"
        else:
            log = logging_time + "데이터 자동 수집 진행"
        logger.set_log(log)
        return 
    
    def update_labeling(case):
        # case N: 미수집 Y: 수집
        logging_time = logger.get_time()
        if case == 'N':
            log = logging_time + "데이터 자동 라벨링 종료"
        else:
            log = logging_time + "데이터 자동 라벨링 진행"
        logger.set_log(log)
        return 

    def update_learning(case):
        # case N: 미사용 Y: 사용
        logging_time = logger.get_time()
        if case == 'N':
            log = logging_time + "모델 자동 학습 종료"
        else:
            log = logging_time + "모델 자동 학습 진행"
        logger.set_log(log)
        return 

    def update_config():
        logging_time = logger.get_time()
        log = logging_time + "환경 설정 수정"
        logger.set_log(log)
        return 

    def get_time():
        now = datetime.datetime.now()
        time = now.strftime("%d/%b/%Y %H:%M:%S")
        logging_time = '[' + time + '] '
        return logging_time
    
    def set_log(log):
        f = open('config/event.log', "a", encoding="UTF-8")
        f.write(log)
        f.write("\n")
        f.close()
        return
