from django.urls import path, include

from businessapp.api.v1.idukaan import api_views as API

org_set = API.OrganizationEmployeeAPIViewset.as_view({
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    #PROD
    path('organization/type/', API.OrganizationTypeListAPIView.as_view()),
    path('organization/', API.AddOrganizationAPIView.as_view()),
    path('organization/list/', API.OrganizationListAPIView.as_view()),
    path('organization/<str:orgid>/', API.OrganizationDetailsAPIView.as_view()),
    path('organization/<str:orgid>/employee/', API.AddOrganizationEmployeeAPIView.as_view()),
    path('organization/<str:orgid>/employee/list/', API.OrganizationEmployeeListAPIView.as_view()),
    path('organization/<str:orgid>/employee/<str:empid>/', org_set),
    #DEV
]