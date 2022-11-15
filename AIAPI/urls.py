from django.urls import path, include
from .views import TestAPI, CAAPI, HFAPI, UserView

urlpatterns = [
    path("test/", TestAPI),
    path("CAmodel/", CAAPI.as_view()),
    path("HFmodel/", HFAPI.as_view()),
    path('UserView/', UserView.as_view()),#User에 관한 API를 처리하는 view로 Request를 넘김
]