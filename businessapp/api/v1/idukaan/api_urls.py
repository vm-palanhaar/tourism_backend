from django.urls import path, include

from businessapp.api.v1.idukaan import api_views as API

org_set = API.OrganizationEmployeeAPIViewset.as_view({
    'patch': 'partial_update',
    'delete': 'destroy'
})

org_state_ops_set = API.OrgStateGstAPIViewset.as_view({
    'post': 'create',
    'get': 'list'
})


urlpatterns = [
    #PROD
    path('org/type/', API.OrganizationTypeListAPIView.as_view()),
    path('org/', API.AddOrganizationAPIView.as_view()),
    path('org/list/', API.OrganizationListAPIView.as_view()),
    path('org/<str:orgid>/', API.OrganizationDetailsAPIView.as_view()),
    path('org/<str:orgid>/emp/', API.AddOrganizationEmployeeAPIView.as_view()),
    path('org/<str:orgid>/emp/list/', API.OrganizationEmployeeListAPIView.as_view()),
    path('org/<str:orgid>/emp/<str:empid>/', org_set),
    #DEV
    path('org/<str:orgid>/gst/', org_state_ops_set),
]