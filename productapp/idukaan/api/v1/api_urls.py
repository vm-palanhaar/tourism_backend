from django.urls import path, include

from productapp.idukaan.api.v1 import api_views as API

urlpatterns = [
    #PROD
    path('org', API.OrgApi.as_view({
        'post' : 'create',
        'get' : 'list',
    })),
    path('brand', API.BrandApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('prod/cat', API.ProductCategoryApi.as_view()),
    path('brand/<str:brandId>/prod', API.BrandProdApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
]