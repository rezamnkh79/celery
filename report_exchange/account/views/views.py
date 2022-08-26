from account.Base.base import Base
import redis
import jwt
import json
from datetime import datetime
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions

from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.contrib.auth import get_user_model

from report_exchange import settings
from account.serializers.serializer import RegisterSerializer, User, UserSerializer
from account.tasks import send_email
from rest_framework import status
from account.models import models

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt import serializers


r = redis.Redis("localhost", 6379, db=0)
if r.get("adtrace_exchange"):
    r.set("adtrace_exchange", "1000000000000")


class Login(TokenViewBase):
    serializer_class = serializers.TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        user = models.User.soft_objects.get_User_by_username(username=request.data["username"])
        if user:
            # Successfully validated so create JWT for login
            return super().post(request, *args, **kwargs)
        else:
            return Response(data={
                "message", "there is no user with this username"
            }, status=status.HTTP_400_BAD_REQUEST)


# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User = get_user_model()
        user = User.objects.create_user(email=request.data["email"], password=request.data["password"],
                                        username=request.data["username"])
        subject, message = Base.welcome_message
        send_email.delay(message, subject, user.email)
        return Response({
            Base.user: UserSerializer(user, context=self.get_serializer_context()).data,
            Base.message: Base.register_message,
        })


def test(request):
    # user = models.User.soft_objects.get_publish("mansourikhah@gmail.com")
    profile = models.Profile.objects.first()
    return HttpResponse(profile.age)


class SendEmailSchedular(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        try:
            token = get_authorization_header(request).decode('utf-8')
            if token is None or token == "null" or token.strip() == "":
                raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')

            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded['user_id']
            user = models.User.soft_objects.get_User_by_id(id=user_id)
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=2,
                period=IntervalSchedule.HOUR)

            PeriodicTask.objects.create(
                interval=schedule,
                name='report exchange {}'.format(datetime.now()),
                task='account.tasks.schedule_send_email',
                kwargs=json.dumps({
                    "email": user.values()[0][Base.email],
                    "message": r.get("adtrace_exchange").decode("utf-8"),
                    "subject": "adtrace exchange is"
                })
            )

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid Token')
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)

        return Response({
            "message": "we will send report of adtrace exchange each two hour"
        }, status=status.HTTP_201_CREATED)





    # def send(request):
    #     subject, message = Base.welcome_message
    #
    #     try:
    #         token = get_authorization_header(request).decode('utf-8')
    #         if token is None or token == "null" or token.strip() == "":
    #             raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')
    #
    #         decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    #         user_id = decoded['user_id']
    #         user = User.objects.get(id=user_id)
    #     except jwt.ExpiredSignature:
    #         raise exceptions.AuthenticationFailed('Token Expired, Please Login')
    #     except jwt.DecodeError:
    #         raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
    #     except jwt.InvalidTokenError:
    #         raise exceptions.AuthenticationFailed('Invalid Token')
    #     except Exception as e:
    #         raise exceptions.AuthenticationFailed(e)
    #     send_email.delay(message, subject, user.email)
    #     return HttpResponse("sent email")

    # def send_exchange(request):
    #     try:
    #         token = get_authorization_header(request).decode('utf-8')
    #         if token is None or token == "null" or token.strip() == "":
    #             raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')
    #
    #         decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    #         user_id = decoded['user_id']
    #         user = User.objects.get(id=user_id)
    #         schedule, created = IntervalSchedule.objects.get_or_create(
    #             every=10,
    #             period=IntervalSchedule.SECONDS)
    #
    #         PeriodicTask.objects.create(
    #             interval=schedule,
    #             name='report exchange {}'.format(datetime.now()),
    #             task='account.tasks.schedule_send_email',
    #             kwargs=json.dumps({
    #                 "email": user.email,
    #                 "message": r.get("adtrace_exchange").decode("utf-8"),
    #                 "subject": "adtrace exchange is"
    #             })
    #         )
    #
    #     except jwt.DecodeError:
    #         raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
    #     except jwt.InvalidTokenError:
    #         raise exceptions.AuthenticationFailed('Invalid Token')
    #     except Exception as e:
    #         raise exceptions.AuthenticationFailed(e)
    #     return HttpResponse("done")

    # try:
    #     token = get_authorization_header(request).decode('utf-8')
    #     if token is None or token == "null" or token.strip() == "":
    #         raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')
    #
    #     decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    #     user_id = decoded['user_id']
    #     user = User.objects.get(id=user_id)
    #     schedule, created = IntervalSchedule.objects.get_or_create(
    #         every=10,
    #         period=IntervalSchedule.SECONDS)
    #
    #     PeriodicTask.objects.create(
    #         interval=schedule,
    #         name='report exchange {}'.format(datetime.now()),
    #         task='account.tasks.schedule_send_email',
    #         kwargs=json.dumps({
    #             "email": user.email,
    #             "message": r.get("adtrace_exchange").decode("utf-8"),
    #             "subject": "adtrace exchange is"
    #         })
    #     )
    #
    # except jwt.DecodeError:
    #     raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
    # except jwt.InvalidTokenError:
    #     raise exceptions.AuthenticationFailed('Invalid Token')
    # except Exception as e:
    #     raise exceptions.AuthenticationFailed(e)
# def login(request):
#     TokenRefreshView.
