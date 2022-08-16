from django.urls import path, include
# from .views import RegisterApi
from . import views

urlpatterns = [
    path('api/register/', views.RegisterApi.as_view()),
    path("send", views.send),
    path("send/exchange", views.send_exchange),
]
