from dashboard.method import ConfigMethod
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import auto_learning
from django.conf import settings

def get_schedule(learning_oper):
    scheduler = getattr(settings,'AUTO_SCHEDULER')

    if learning_oper == 'Y':
        config_data = ConfigMethod.get()

        learning_cycle = config_data.learning_cycle
        learning_start = config_data.learning_start
        start_date = config_data.start_date

        job_list = scheduler.get_jobs()
        print(job_list)

        if len(job_list) != 0:
            scheduler.shutdown()

        print("Set up Schedule")

        # 코드 테스트용
        # 1시간에 한번씩 실행
        # if learning_cycle =='1D':
        #     scheduler.add_job(auto_learning, 'cron', id='auto_learning' ,hour=learning_start)
        # elif learning_cycle == '1W':
        #     weekday = start_date.weekday()
        #     scheduler.add_job(auto_learning, 'cron', id='auto_learning' ,day_of_week=weekday, hour=learning_start)
        # elif learning_cycle == '1M':
        #     day = start_date.day
        #     scheduler.add_job(auto_learning, 'cron', id='auto_learning' ,day=day, hour=learning_start)

        scheduler.add_job(auto_learning, 'cron', id='auto_learning' ,hour='0-23')
        # 테스트용 종료(위에거랑 교체해야함)

        scheduler.start()
        print("Start auto learning")

    else:
        print("Stop auto learning")
        scheduler.pause()

    return
