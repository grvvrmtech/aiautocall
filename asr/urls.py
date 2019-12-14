# howdy/urls.py
from django.urls import path
from asr import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('index.html/', views.HomePageView.as_view()),
    path('rules.html/', views.RulesPageView.as_view()),
    path('register.html', views.RegisterPageView.as_view(), name='register'),
    path('upload/', views.uploadAudio),
    path('index.html/upload/', views.uploadAudio),
    path('get_text/', views.getText),
    path('index.html/get_text/', views.getText),
    path('check_key/', views.checkKey),
    path('index.html/check_key/', views.checkKey),
    path('register/', views.registerUser, name='registeruser'),
    path('register.html/register/', views.registerUser),
]
