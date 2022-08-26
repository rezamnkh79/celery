from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from account.models.models import Profile



User = get_user_model()

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists!")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists!")
        return value

    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'],
    #                                     first_name=validated_data['first_name'],
    #                                     last_name=validated_data['last_name'],
    #                                     email=serializers.EmailField(
    #                                         validators=[UniqueValidator(queryset=User.objects.all())])
    #                                     )
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['age','phone_number']



# class EmailSerializers(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=50, min_length=5)
#     password = serializers.CharField(min_length=8, max_length=30)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password')
#
#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("A user with this email already exists!")
#         return value
#

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)
#
#         # Add custom claims
#         token['username'] = user.username
#         return token
