from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import login

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from knox.models import AuthToken

from userapp import serializers, models, permissions
from userapp.api import errors as UserError

'''
PROD
1. UserRegisterAPIView
2. UserLoginAPIView
3. UserProfileAPIView

DEV
'''

def response_200(response_data):
    return Response(response_data, status=status.HTTP_200_OK)

def response_400(response_data):
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

def response_401(response_data):
    return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

def response_409(response_data):
    return Response(response_data, status=status.HTTP_409_CONFLICT)


class UserRegisterApi(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        if 'username' not in request.data or 'email' not in request.data == None:
            return response_400(UserError.userEmptyFields())
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #TODO: Email verification to user
            response_data['user'] = serializer.data
            response_data['message'] = 'We are happy to on-board you. Please check registered mail for account verification link.'
            return Response(response_data,status=status.HTTP_201_CREATED)
        if 'username' in serializer.errors and 'email' in serializer.errors:
            return response_409(UserError.userUsernameEmailFound())
        elif 'username' in serializer.errors:
            return response_409(UserError.userUsernameFound())
        elif 'email' in serializer.errors:
            return response_409(UserError.userEmailFound())
        elif 'password' in serializer.errors:
            return response_409(UserError.userPwdCommon())
        return response_400(serializer.errors)
        


class UserLoginApi(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        try:
            user = models.User.objects.get(username = request.data['username'])
        except models.User.DoesNotExist:
            return response_400(UserError.userInvalid())
        if user.is_active == False:
            #TODO: Email verification to user
            return response_400(UserError.userInActive())
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            response_data['user'] = serializer.data
            response_data['token'] = AuthToken.objects.create(user)[1]
            return Response(response_data, status=status.HTTP_200_OK)
        return response_400(UserError.userInvalidCred())


class UserProfileApi(generics.RetrieveAPIView, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,permissions.IsVerified]

    def get(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(username = request.user)
        except models.User.DoesNotExist:
            return response_400(UserError.userInvalid())
        serializer = serializers.UserSerializer(user)
        return response_200(serializer.data)
