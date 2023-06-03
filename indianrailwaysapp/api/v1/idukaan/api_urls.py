from django.urls import path, include

from indianrailwaysapp.api.v1.idukaan import api_views as API

org_shop_api_set = API.OrgShopApi.as_view({
    'post': 'create',
    'get': 'list',
    'patch': 'partial_update',
    'get': 'retrieve'
})


org_shop_emp_patch_delete_set = API.OrgShopEmpPatchDeleteAPIViewset.as_view({
    'patch': 'partial_update',
    'delete': 'destroy'
})

org_shop_license_set = API.ShopLicenseAPIViewset.as_view({
    'post': 'create',
    'get': 'list'
})

org_shop_fssai_license_set = API.ShopFssaiLicenseAPIViewset.as_view({
    'post': 'create',
    'get': 'list'
})

org_shop_inv_set = API.ShopInventoryPatchDeleteAPIViewset.as_view({
    'patch': 'partial_update',
    'delete': 'destroy'
})

org_shop_gst = API.ShopGstPostGetAPIViewset.as_view({
    'post': 'create',
    'get': 'list'
})

urlpatterns = [
    path('org/', include([
        path('<str:orgId>/', include([
            #PROD
            path('shop/', org_shop_api_set),
            path('shop/<str:shopId>/emp/', API.AddOrgShopEmpAPIView.as_view()),
            path('shop/<str:shopid>/emp/list/', API.OrgShopEmpListAPIView.as_view()),
            path('shop/<str:shopid>/emp/<str:empid>/', org_shop_emp_patch_delete_set),

            path('shop/<str:shopid>/lic/', org_shop_license_set),
            path('shop/<str:shopid>/fssai-lic/', org_shop_fssai_license_set),

            path('shop/<str:shopid>/inv/', API.AddShopInventoryAPIView.as_view()),
            path('shop/<str:shopid>/inv/stock', API.ShopInventoryListAPIView.as_view()),
            path('shop/<str:shopid>/inv/<str:invid>/', org_shop_inv_set),

            path('shop/<str:shopid>/gst/', org_shop_gst),

            #DEV
        ])),
        path('shop/list/', API.ShopListAPIView.as_view()),
        #DEV
    ])),
    path('shop/type/', API.ShopBusinessTypesApi.as_view()),
    #DEV
]