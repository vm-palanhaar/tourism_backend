from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import login

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken

from userapp import serializers, models

'''
PROD
1. UserRegisterAPIView
2. UserLoginAPIView
3. UserProfileAPIView

DEV
'''

failed_response_map = {'error':None}
response_map = {"data":None}

error_user_invalid = {
    'code' : 'user_invalid',
    'message' : ''
}

error_user_invalid_cred = {
    'code' : 'user_invalid_cred',
    'message' : ''
}

error_user_active = {
    'code' : 'user_active',
    'message' : ''
}



class UserRegisterApi(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #TODO: Email verification to user
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class UserLoginApi(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(username = request.data['username'])
        except models.User.DoesNotExist:
            return Response(error_user_invalid, status=status.HTTP_400_BAD_REQUEST)
    
        if user.is_active == False:
            #TODO: Email verification to user
            return Response(error_user_active, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            response_data = {
                'user' : serializer.data,
                'token' : AuthToken.objects.create(user)[1]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(error_user_invalid_cred, status=status.HTTP_400_BAD_REQUEST)


class UserProfileApi(generics.RetrieveAPIView, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(username = request.user, is_active=True)
        except models.User.DoesNotExist:
            return Response(error_user_invalid, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
