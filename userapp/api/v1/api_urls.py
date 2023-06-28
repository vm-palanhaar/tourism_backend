from django.urls import path

from userapp.api.v1 import api_views as APIv1
from knox import views as knox_views


urlpatterns = [
    #PROD
    path('register', APIv1.UserRegisterApi.as_view()),
    path('login', APIv1.UserLoginApi.as_view()),
    path('profile', APIv1.UserProfileApi.as_view()),
    path('logout', knox_views.LogoutView.as_view()),
    path('logoutAll', knox_views.LogoutAllView.as_view()),
    #DEV
]