from django.urls import path, include

from businessapp.idukaan.api.v1 import api_views as API

urlpatterns = [
    #PROD
    path('org/type', API.OrgTypesApi.as_view()),
    path('org', API.OrgApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('org/<str:orgId>', API.OrgApi.as_view({
        'get': 'retrieve',
    })),
    path('org/<str:orgId>/emp', API.OrgEmpApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('org/<str:orgId>/emp/<str:orgEmpId>', API.OrgEmpApi.as_view({
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
    path('org/<str:orgId>/gst', API.OrgStateGstApi.as_view({
        'post': 'create',
        'get': 'list'
    })),
    #DEV
]