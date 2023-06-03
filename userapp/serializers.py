from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from userapp import models as UserModel

from knox.models import AuthToken

'''
Common APIs Serializer
1. UserRegisterSerializer
2. UserLoginSerializer
3. UserLoginResponseSerializer
4. UserSerializer

Yatrigan APIs Serializer

iDukaan APIs Serializer

'''


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=UserModel.User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = UserModel.User
        fields = ('username','password','email','first_name','last_name','contact_number')

        #raise serializers.ValidationError({"password": "Password fields didn't match."})

    def create(self, validated_data):
        user = UserModel.User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            contact_number = validated_data['contact_number']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError()


class UserLoginResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = UserModel.User
        fields = ['username','first_name','token','is_verified']
    
    def get_token(self, instance): 
        return AuthToken.objects.create(instance)[1]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel.User
        fields = ['first_name','last_name','username','email','contact_number']
