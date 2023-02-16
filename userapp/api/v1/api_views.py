from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import login

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from userapp import serializers, models

'''
PROD
1. UserRegisterAPIView
2. UserLoginAPIView
3. UserProfileAPIView

DEV
'''


response_map = {"data":None}

login_failed_user_not_exist = 'User does not exist. Click on Sign Up button to register.'
login_failed_user_not_active = 'User not active! Please check registered mail for verification link.'
login_failed_user_invalid_credentials = 'Invalid username or password'

profile_failed_user_not_exist = 'Something went wrong. Please login again to continue.'


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #TODO: Email verification to user
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(username = request.data['username'])
        except models.User.DoesNotExist:
            response_map['data'] = login_failed_user_not_exist
            return Response(response_map, status=status.HTTP_400_BAD_REQUEST)
    
        if user.is_active == False:
            #TODO: Email verification to user
            response_map['data'] = login_failed_user_not_active
            return Response(response_map, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response(serializers.UserLoginResponseSerializer(user).data)
        
        response_map['data'] = login_failed_user_invalid_credentials
        return Response(response_map, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.GenericAPIView, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(username = request.user)
        except models.User.DoesNotExist:
            response_map['data'] = profile_failed_user_not_exist
            return Response(response_map, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(user)
        response_map['data'] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)
