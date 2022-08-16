from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response

from account.serializers.serializer import RegisterSerializer, UserSerializer
from .tasks import send_email, schedule_send_email
from account.Base.base import Base
import redis
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from datetime import datetime
import json

r = redis.Redis("localhost", 6379, db=0)
if r.get("adtrace_exchange") == None:
    r.set("adtrace_exchange", "1000000000000")


# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(request.data)
        return Response({
            Base.user: UserSerializer(user, context=self.get_serializer_context()).data,
            Base.message: Base.register_message,
        })


from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
import jwt
from celery_project import settings
from django.contrib.auth.models import User


def send(request):
    subject, message = Base.welcome_message

    try:
        token = get_authorization_header(request).decode('utf-8')
        if token is None or token == "null" or token.strip() == "":
            raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')

        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded['user_id']
        user = User.objects.get(id=user_id)
    except jwt.ExpiredSignature:
        raise exceptions.AuthenticationFailed('Token Expired, Please Login')
    except jwt.DecodeError:
        raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid Token')
    except Exception as e:
        raise exceptions.AuthenticationFailed(e)
    send_email.delay(message, subject, user.email)
    return HttpResponse("sent email")


def run(request):
    v = schedule_send_email.delay()
    return HttpResponse(v)


print(r.get("adtrace_exchange"))
# # Create your views here.
# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#
#         return Response(content)
#
#
# from .serializer import MyTokenObtainPairSerializer
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
#
#
# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer
#
from celery_project import celery


def send_exchange(request):
    try:
        token = get_authorization_header(request).decode('utf-8')
        if token is None or token == "null" or token.strip() == "":
            raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')

        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded['user_id']
        user = User.objects.get(id=user_id)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS)

        PeriodicTask.objects.create(
            interval=schedule,
            name='report exchange {}'.format(datetime.now()),
            task='account.tasks.schedule_send_email',
            kwargs=json.dumps({
                "email": user.email,
                "message": "this is a test email",
                "subject": "subject"
            })
        )

    except jwt.DecodeError:
        raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid Token')
    except Exception as e:
        raise exceptions.AuthenticationFailed(e)
    return HttpResponse("done")
