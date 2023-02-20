from django.urls import path, include

from indianrailwaysapp.api.v1.idukaan import api_views as API

org_shop_patch_get_set = API.OrgshopPatchDetailsAPIViewset.as_view({
    'patch': 'partial_update',
    'get': 'retrieve'
})

org_shop_emp_patch_delete_set = API.OrgShopEmpPatchDeleteAPIViewset.as_view({
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    #PROD
    path('org/', include([
        #PROD
        path('<str:orgid>/', include([
            #PROD
            path('shop/', API.AddShopAPIView.as_view()),
            path('shop/list/', API.OrgShopListAPIView.as_view()),
            path('shop/<str:shopid>/', org_shop_patch_get_set),
            path('shop/<str:shopid>/emp/', API.AddOrgShopEmpAPIView.as_view()),
            path('shop/<str:shopid>/emp/list/', API.OrgShopEmpListAPIView.as_view()),
            path('shop/<str:shopid>/emp/<str:empid>/', org_shop_emp_patch_delete_set),
            #DEV
        ])),
        path('shop/list/', API.ShopListAPIView.as_view()),
        #DEV
    ])),
    #DEV
]