from django.urls import path, include

from indianrailwaysapp.api.v1.idukaan import api_views as API

org_shop_gst = API.ShopGstApi.as_view({
    'post': 'create',
    'get': 'list'
})

urlpatterns = [
    path('org/', include([
        path('<str:orgId>/', include([
            #PROD
            path('shop', API.OrgShopApi.as_view({
                'post': 'create',
                'get': 'list'
            })),
            path('shop/<str:shopId>', API.OrgShopApi.as_view({
                'patch': 'partial_update',
                'get': 'retrieve'
            })),
            path('shop/<str:shopId>/emp', API.OrgShopEmpAPi.as_view({
                'post': 'create',
                'get': 'list'
            })),
             path('shop/<str:shopId>/emp/<str:empId>', API.OrgShopEmpAPi.as_view({
                'patch': 'partial_update',
                'delete': 'destroy'
            })),
            path('shop/<str:shopId>/lic', API.ShopLicApi.as_view({
                'post': 'create',
                'get': 'list'
            })),
            path('shop/<str:shopId>/fssaiLic', API.ShopFssaiLicApi.as_view({
                'post': 'create',
                'get': 'list'
            })),

            path('shop/<str:shopId>/inv', API.ShopInvApi.as_view({
                'post': 'create',
                'get': 'list'
            })),
            path('shop/<str:shopId>/inv/<str:invId>',  API.ShopInvApi.as_view({
                'patch': 'partial_update',
                'delete': 'destroy'
            })),

            path('shop/<str:shopId>/gst', org_shop_gst),

            #DEV
        ])),
        path('shop', API.ShopListApi.as_view()),
        #DEV
    ])),
    path('shop/type', API.ShopBusinessTypesApi.as_view()),
    #DEV
]