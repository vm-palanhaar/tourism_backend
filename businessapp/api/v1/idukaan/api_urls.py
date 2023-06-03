from django.urls import path, include

from businessapp.api.v1.idukaan import api_views as API


org_api_set = API.OrgApi.as_view({
    'post': 'create',
    'get': 'list',
})

org_emp_api_set = API.OrgEmpApi.as_view({
    'post': 'create',
    'get': 'list',
    'patch': 'partial_update',
    'delete': 'destroy'
})

org_state_ops_set = API.OrgStateGstAPIViewset.as_view({
    'post': 'create',
    'get': 'list'
})


urlpatterns = [
    #PROD
    path('type/org/', API.OrgTypesApi.as_view()),
    path('org/', org_api_set),
    path('org/<str:orgId>/emp/', org_emp_api_set),
    path('org/<str:orgId>/gst/', org_state_ops_set),
    #DEV
]