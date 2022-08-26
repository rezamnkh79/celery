from django.urls import path, include
# from .views import RegisterApi
from account.views import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view()),
    path('login', views.Login.as_view()),
    path("send/exchange", views.SendEmailSchedular.as_view()),
    path("test",views.test)
]
