from django.urls import path
from .views import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


app_name = "main"
urlpatterns = [
    path("login/", LoginView.as_view(template_name='main/main.html'), name='login'),
    # path("login/", login.as_view()),
]