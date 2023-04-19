import re, math

from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, viewsets

from productapp import models as PCModel
from productapp import serializers as PCSerializer


'''
PROD
1. AddBrandAPIView
2. BrandListSearchAPIView
3. BrandListAPIView
4. ProductCategoryListAPIView
5. AddProductAPIView
6. ProductListAPIView
7. ProductAPIViewset
DEV
'''

failed_response_map = {'error':None}
response_map = {'data':None}

is_error = 'Something went wrong. Issue reported to Team and your account will be de-activated.'

brands_search_not_found = 'Brands not registered!'
brands_active_not_found = 'Brands not registered or verification in-progress!'
brands_in_active_not_found = 'Brands not registered or verification completed!'

product_add_brand_not_found = 'Brand not registered or not active!'
product_search_brand_not_found = 'Products not registered!'
products_active_not_found = 'Products not registered or verification in-progress!'
products_in_active_not_found = 'Products not registered or verification completed!'
product_delete_not_applicable = 'Product deletion not allowed!'
product_update_not_applicable = 'Product modification not allowed!'


def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


class AddBrandAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    queryset = PCModel.Brand.objects.all()
    serializer_class = PCSerializer.AddBrandSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.data['confirm'] == 'false':
            brands = PCModel.Brand.objects.filter(name__icontains=request.data['name'], is_show=True)
            if brands.count() != 0 :
                serializer = PCSerializer.BrandListSerializer(brands, many=True)
                response_map['data'] = serializer.data
                return Response(response_map, status=status.HTTP_200_OK)
        return super().post(request, *args, **kwargs)
    

class BrandListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = PCSerializer.BrandListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if len(re.findall("\d",request.GET.get('page'))) == 0 or int(request.GET.get('page')) == 0:
            return error_response(is_error)
        
        page_num = int(request.GET.get('page'))
        is_failure = brands_search_not_found

        if request.GET.get('search',None) != None:
            brands = PCModel.Brand.objects.filter(name__icontains=request.GET.get('search',None), is_show=True)
        else:
            brands = PCModel.Brand.objects.filter(is_show=True)

        #To check for active filter 0:False and 1:True
        if request.GET.get('active',None) != None:

            if request.GET.get('active',None) == '1':
                brands = brands.filter(is_active=True)
                is_failure = brands_active_not_found
            elif request.GET.get('active',None) == '0':
                brands = brands.filter(is_active=False)
                is_failure = brands_in_active_not_found
                    
        #To check for total number of brands object
        if brands.count() == 0:
            failed_response_map['error'] = is_failure
            return Response(failed_response_map, status=status.HTTP_200_OK)

        serializer = self.get_serializer(brands, many=True)
        from_range = 1 if page_num == 1 else ((page_num-1)*15)+1
        to_range = (page_num)*15 if (page_num)*15 < brands.count() else brands.count()
        response_map['data'] = {
            'pages' : math.ceil(brands.count()/15),
            'message' : f'Showing list of brands from {from_range} to {to_range} out of {brands.count()}',
            'alert' : None if to_range!=brands.count() else 'No more brands to show',
            'results' : serializer.data[(page_num-1)*15: (page_num)*15],
        }
        return Response(response_map, status=status.HTTP_200_OK)


class ProductCategoryListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    queryset = PCModel.ProductCategory.objects.all()
    serializer_class = PCSerializer.ProductCategoryListSerializer
    permission_classes = [IsAuthenticated]


class AddProductAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    serializer_class = PCSerializer.AddProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if kwargs['brandid'] != request.data['brand']:
            failed_response_map['error'] = is_error
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data['confirm'] == 'false':
            try:
                PCModel.Brand.objects.get(id=request.data['brand'])
            except PCModel.Brand.DoesNotExist:
                failed_response_map['error'] = product_add_brand_not_found
                return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        
            products = PCModel.Product.objects.filter(brand = request.data['brand'],
                                                        name__icontains=request.data['name'])
            if products.count() != 0 :
                serializer = PCSerializer.ProductListSerializer(products, many=True)
                response_map['data'] = serializer.data
                
                return Response(response_map, status=status.HTTP_200_OK)
                
        return super().post(request, *args, **kwargs)


class BrandProductListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = PCSerializer.ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            brand = PCModel.Brand.objects.get(id=kwargs['brandid'])
        except PCModel.Brand.DoesNotExist:
            error_response(is_error)
        
        if len(re.findall("\d",request.GET.get('page'))) == 0 or int(request.GET.get('page')) == 0:
            return error_response(is_error)
        
        page_num = int(request.GET.get('page'))
        is_failure = product_search_brand_not_found

        if request.GET.get('search',None) != None:
            products = PCModel.Product.objects.filter(brand=brand, name__icontains=request.GET.get('search',None))
        else:
            products = PCModel.Product.objects.filter(brand=brand)

        #To check for active filter 0:False and 1:True
        if request.GET.get('active',None) != None:

            if request.GET.get('active',None) == '1':
                products = products.filter(is_active=True)
                is_failure = products_active_not_found
            elif request.GET.get('active',None) == '0':
                products = products.filter(is_active=False)
                is_failure = products_in_active_not_found
        
        #To check for total number of brands object
        if products.count() == 0:
                failed_response_map['error'] = is_failure
                return Response(failed_response_map, status=status.HTTP_200_OK)

        serializer = self.get_serializer(products, many=True)
        from_range = 1 if page_num == 1 else ((page_num-1)*5)+1
        to_range = (page_num)*5 if (page_num)*5 < products.count() else products.count()
        response_map['data'] = {
            'pages' : math.ceil(products.count()/5),
            'message' : f'Showing list of {brand.name} products from {from_range} to {to_range} out of {products.count()}',
            'alert' : None if to_range!=products.count() else 'No more products to show',
            'results' : serializer.data[(page_num-1)*5: (page_num)*5],
        }
        return Response(response_map, status=status.HTTP_200_OK)


class ProductAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        try:
            product = PCModel.Product.objects.get(id=kwargs['productid'])
        except PCModel.Product.DoesNotExist:
            failed_response_map['error'] = is_error
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
    
        if product.brand.is_show == True:
            failed_response_map['error'] = product_update_not_applicable
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = PCSerializer.PatchProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            product = PCModel.Product.objects.get(id=kwargs['productid'])
            serializer = PCSerializer.ProductSerializer(product)
            response_map['data'] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


    def destroy(self, request, *args, **kwargs):
        try:
            product = PCModel.Product.objects.get(id=kwargs['productid'])
        except PCModel.Product.DoesNotExist:
            failed_response_map['error'] = is_error
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        
        if product.brand.is_show == True:
            failed_response_map['error'] = product_delete_not_applicable
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
