from django.conf.urls import url
from django.urls import path, include
from .api import RegisterApi
from . import views
urlpatterns = [
      path('api/register/', RegisterApi.as_view()),
      path("send",views.send)
]
