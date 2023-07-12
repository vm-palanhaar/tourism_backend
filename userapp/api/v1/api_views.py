from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import login

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken

from userapp import serializers, models
from userapp.api import errors as UserError

'''
PROD
1. UserRegisterAPIView
2. UserLoginAPIView
3. UserProfileAPIView

DEV
'''

class UserRegisterApi(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        if request.data['username'] == None or request.data['email'] == None or request.data['password'] == None:
            response_data['error'] = UserError.error_user_fields_empty
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #TODO: Email verification to user
            response_data['user'] = serializer.data
            response_data['message'] = 'We are happy to on-board you. Please check registered mail for account verification link.'
            return Response(response_data,status=status.HTTP_201_CREATED)
        if 'username' in serializer.errors and 'email' in serializer.errors:
            response_data['error'] = UserError.error_user_username_email_found
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        elif 'username' in serializer.errors:
            response_data['error'] = UserError.error_user_username_found
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        elif 'email' in serializer.errors:
            response_data['error'] = UserError.error_user_email_found
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        elif 'password' in serializer.errors:
            response_data['error'] = UserError.error_user_password_common
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class UserLoginApi(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        try:
            user = models.User.objects.get(username = request.data['username'])
        except models.User.DoesNotExist:
            response_data['error'] = UserError.error_user_invalid
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
        if user.is_active == False:
            #TODO: Email verification to user
            response_data['error'] = UserError.error_user_inactive
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            response_data['user'] = serializer.data
            response_data['token'] = AuthToken.objects.create(user)[1]
            return Response(response_data, status=status.HTTP_200_OK)
        response_data['error'] = UserError.error_user_invalid_cred
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UserProfileApi(generics.RetrieveAPIView, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(username = request.user, is_active=True)
        except models.User.DoesNotExist:
            return Response(UserError.error_user_invalid, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
