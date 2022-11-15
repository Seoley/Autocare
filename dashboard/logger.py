import datetime

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