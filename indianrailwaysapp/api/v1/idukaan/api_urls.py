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

            path('shop/<str:shopid>/license/', org_shop_license_set),
            path('shop/<str:shopid>/fssailicense/', org_shop_fssai_license_set),

            path('shop/<str:shopid>/inv/', API.AddShopInventoryAPIView.as_view()),
            path('shop/<str:shopid>/inv/stock', API.ShopInventoryListAPIView.as_view()),
            path('shop/<str:shopid>/inv/<str:invid>/', org_shop_inv_set),

            path('shop/<str:shopid>/gst/', org_shop_gst),

            #DEV
        ])),
        path('shop/list/', API.ShopListAPIView.as_view()),
        #DEV
    ])),
    path('shop/type/', API.ShopBusinessTypeListAPIView.as_view()),
    #DEV
]