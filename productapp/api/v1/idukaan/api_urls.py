from django.urls import path, include

from productapp.api.v1.idukaan import api_views as API


urlpatterns = [
    #PROD
    path('brand', API.BrandApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('product/cat', API.ProductCategoryApi.as_view()),
    path('brand/<str:brandId>/product', API.BrandProdApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('brand/<str:brandId>', API.BrandProdGroupApi.as_view()),
    #DEV
    # path('product/<str:productId>', API.BrandProdApi.as_view({
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # })),
]