from django.urls import path, include
# from .views import RegisterApi
from account.views import views

urlpatterns = [
    path('api/register/', views.RegisterApi.as_view()),
    path("send/exchange", views.SendEmailSchedular.as_view()),

]
