from dashboard.models import CrCompany, CrConfig, CrModelInfo, CrModelHistory
from django.db.models import Q


class CompanyMethod():
    def get(company_name):
        
        Company_list = CrCompany.objects.filter(
            Q(company_name__icontains=company_name)
        )

        return Company_list

    def set(company_name, company_ip, company_token, company_operation):
        print("Method")
        company = CrCompany(company_name=company_name, company_ip=company_ip, company_token=company_token, company_operation=company_operation)
        company.save()

        return

class ConfigMethod():
    #프로토타입에서는 config 테이블에서 첫 번째 줄 값만 사용
    #이후 공개배포를 할 때에는 이 부분에 대한 유지보수 진행 필요 있음

    def get():
        config_data = CrConfig.objects.all()[0]
        return config_data
    def set(collection_oper=None, labeling_oper=None, learning_oper=None, learning_cycle=None, learning_start=None):
        
        config_data = CrConfig.objects.all()[0] #프로토타입에서는 config 테이블에서 첫 번째 줄 값만 사용

        if collection_oper is not None:
            config_data.collection_oper = collection_oper
        if labeling_oper is not None:
            config_data.labeling_oper = labeling_oper
        if learning_oper is not None:
            config_data.learning_oper = learning_oper
        if learning_cycle is not None:
            config_data.learning_cycle = learning_cycle
        if learning_start is not None:
            config_data.learning_start = learning_start

        config_data.save()
        
        return

class ModelMethod():
    def get(model_id=None):
        if model_id is not None:
            model_data = CrModelInfo.objects.filter(model_id=model_id)[0]
        
        return model_data
    
    def set(model_id, model_name=None, model_rname=None, model_path=None, model_api=None, data_path=None, model_file = None):

        model_data = CrModelInfo.objects.filter(model_id=model_id)[0]

        if model_name is not None:
            model_data.model_name = model_name
        if model_rname is not None:
            model_data.model_rname = model_rname
        if model_path is not None:
            model_data.model_path = model_path
        if model_api is not None:
            model_data.model_api = model_api
        if data_path is not None:
            model_data.data_path = data_path
        if model_file is not None:
            model_data.model_file = model_file

        model_data.save()
        return