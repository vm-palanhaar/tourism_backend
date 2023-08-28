from django.urls import path, include

from productapp.api.v1.idukaan import api_views as API


urlpatterns = [
    #PROD
    path('org', API.OrgApi.as_view({
        'post' : 'create'
    })),
    path('brand', API.BrandApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('product/cat', API.ProductCategoryApi.as_view()),
    path('brand/<str:brandId>/product', API.BrandProdApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    #DEV
    # path('product/<str:productId>', API.BrandProdApi.as_view({
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # })),
]