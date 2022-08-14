from django.shortcuts import render

from rest_framework.views import APIView


from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
# Create your views here.
class HelloView(APIView):

    permission_classes = (IsAuthenticated,)


    def get(self, request):

        content = {'message': 'Hello, World!'}

        return Response(content)


from .serializer import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

from django.core.mail import send_mail
from django.conf import settings

def send(request):

        subject, msg = "hello","message"

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["rezamansourikhah@gmail.com"]
        )