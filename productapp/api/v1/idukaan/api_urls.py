from django.urls import path, include

from productapp.api.v1.idukaan import api_views as API

product_set = API.ProductAPIViewset.as_view({
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    #PROD
    path('brand/', API.AddBrandAPIView.as_view()),
    path('brand/list/', API.BrandListAPIView.as_view()),
    path('category/', API.ProductCategoryListAPIView.as_view()),
    path('brand/<str:brandid>/group/', API.ProductGroupListAPIView.as_view()),
    path('brand/<str:brandid>/subgroup/<str:subgroupid>/', API.ProductSubGroupAPIView.as_view()),
    path('brand/<str:brandid>/product/', API.AddProductAPIView.as_view()),
    path('brand/<str:brandid>/product/list/', API.BrandProductListAPIView.as_view()),
    path('brand/product/<str:productid>/', product_set),
    #DEV
]