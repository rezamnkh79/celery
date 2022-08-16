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

from django.contrib.auth.models import User
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from report_exchange import settings
from account.serializers.serializer import RegisterSerializer, UserSerializer
from .tasks import send_email, schedule_send_email

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
    return HttpResponse("done")
