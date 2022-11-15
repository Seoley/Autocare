from django.urls import path
from .views import autocareinfo, autocareconfig, autocarecompany
from .controler import company_control, config_control, info_control

urlpatterns = [
    path("info/", autocareinfo.as_view()),
    path("config/", autocareconfig.as_view()),
    path("company/", autocarecompany.as_view()),

    path("company_set/", company_control.company_set),
    path("company_search/", company_control.company_search),

    path("setting_save/", config_control.setting_save),
    path("collection_set/<str:collection_oper>/", config_control.collection_set),
    path("labeling_set/<str:labeling_oper>/", config_control.labeling_set),
    path("learning_set/<str:learning_oper>/", config_control.learning_set),

    path("do_learning/", info_control.do_learning),

    # path("company_search/", company_control.company_search)
]