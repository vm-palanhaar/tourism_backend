from django.urls import path, include

from mobileapp.api.v1 import api_views as API


urlpatterns = [
    #PROD
    path('feedback/', API.MobileAppFeedbackAPIView.as_view()),
    #DEV
]