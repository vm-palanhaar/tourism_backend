import re, math

from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, viewsets

from userapp import permissions as UserPerm
from productapp import models as PCModel
from productapp import serializers as PCSerializer
from productapp.api.v1 import errors as PcError

from apiutil import errors as UtilError


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

def response_200(response_fail):
    return Response(response_fail, status=status.HTTP_200_OK)

def response_400(response_fail):
    return Response(response_fail, status=status.HTTP_400_BAD_REQUEST)

def response_401(response_fail):
    return Response(response_fail, status=status.HTTP_401_UNAUTHORIZED)

def response_409(response_fail):
    return Response(response_fail, status=status.HTTP_409_CONFLICT)


class BrandApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated, UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['brandName'] = request.data['name']
        if request.data['confirm'] == 'false':
            brands = PCModel.Brand.objects.filter(name__icontains=request.data['name'], is_show=True)
            if brands.count() != 0 :
                serializer = PCSerializer.BrandListSerializer(brands, many=True)
                response_data['brandList'] = serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
        serializer = PCSerializer.AddBrandSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data['message'] = 'We appreciate for your efforts for making our community a better place to visit and shop at your store. '\
            'We thrive building a community to promote local products and the manufacturers to recognize themselves through Made In India initiative.'
            return Response(response_data, status=status.HTTP_201_CREATED)
        return response_400(serializer.errors)
    
    def list(self, request, *args, **kwargs):
        response_data = {}
        if len(re.findall("\d",request.GET.get('page'))) == 0 or int(request.GET.get('page')) < 1:
            response_data.update(UtilError.badActionUser(request, 'BrandApiList_Page_Url-{0}'.format(request.GET.get('page'))))
            return response_401(response_data)
        page_num = int(request.GET.get('page'))
        # To check for search filter
        if request.GET.get('search',None) != None:
            brands = PCModel.Brand.objects.filter(name__icontains=request.GET.get('search',None), is_show=True)
            is_failure = PcError.pcBrandSearchListEmpty(request.GET.get('search',None))
        else:
            brands = PCModel.Brand.objects.filter(is_show=True)
            is_failure = PcError.pcBrandListEmpty()
        # To check for active filter 0:False and 1:True
        if request.GET.get('active',None) != None:
            if request.GET.get('active',None) == '1':
                brands = brands.filter(is_active=True)
                is_failure = PcError.pcBrandActiveListEmpty()
            elif request.GET.get('active',None) == '0':
                brands = brands.filter(is_active=False)
                is_failure = PcError.pcBrandInActiveListEmpty()       
        # To check for total number of brands object
        if brands.count() == 0:
            response_data.update(is_failure)
            return response_400(response_data)
        serializer = PCSerializer.BrandListSerializer(brands, many=True)
        from_range = 1 if page_num == 1 else ((page_num-1)*15)+1
        to_range = (page_num)*15 if (page_num)*15 < brands.count() else brands.count()
        response_data = {
            'pages' : math.ceil(brands.count()/15),
            'message' : f'Showing list of brands from {from_range} to {to_range} out of {brands.count()}',
            'alert' : None if to_range!=brands.count() else 'No more brands found in the community.',
            'brandList' : serializer.data[(page_num-1)*15: (page_num)*15],
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ProductCategoryApi(generics.ListAPIView, PermissionRequiredMixin):
    queryset = PCModel.ProductCategory.objects.all()
    serializer_class = PCSerializer.ProductCategoryListSerializer
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]


class BrandProdApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['brandId'] = str(request.data['brand'])
        if kwargs['brandId'] == str(request.data['brand']):
            if request.data['confirm'] == 'false':
                products = PCModel.Product.objects.filter(brand=request.data['brand'], name__icontains=request.data['name'])
                if products.count() != 0:
                    serializer = PCSerializer.ProductListSerializer(products, many=True)
                    response_data['prodList'] = serializer.data
                    return response_200(response_data)
            serializer = PCSerializer.AddProductSerializer(data = request.data, context={'images': request.FILES.getlist('images')})
            if serializer.is_valid():
                serializer.save()
                response_data['message'] = 'We appreciate for your efforts for making our community a better place to visit and shop at your store. '\
                'We thrive building a community to promote local products and the manufacturers to recognize themselves through Made In India initiative.'
                return Response(response_data, status=status.HTTP_201_CREATED)
            return response_400(serializer.errors)
        response_data.update(UtilError.badActionUser(request,'BrandProdApiCreate_brandId_Url-{0}_HB-{1}'.format(kwargs['brandId'], request.data['brand'])))
        return response_401(response_data)

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['brandId'] = kwargs['brandId']
        if len(re.findall("\d",request.GET.get('page'))) == 0 or int(request.GET.get('page')) == 0:
            response_data.update(UtilError.badActionUser(request, 'BrandProdApiList_Page_Url-{0}'.format(request.GET.get('page'))))
            return response_401(response_data)
        try:
            brand = PCModel.Brand.objects.get(id=kwargs['brandId'])
        except PCModel.Brand.DoesNotExist:
            response_data.update(PcError.pcBrandNotFound())
            return response_400(response_data)
        page_num = int(request.GET.get('page'))
        # To check for search filter
        if request.GET.get('search',None) != None:
            products = PCModel.Product.objects.filter(brand=brand, name__icontains=request.GET.get('search',None))
            is_failure = PcError.pcBrandProdSearchListEmpty(request.GET.get('search',None), brand.name)
        else:
            products = PCModel.Product.objects.filter(brand=brand)
            is_failure = PcError.pcBrandProdListEmpty(brand.name)
        # To check for active filter 0:False and 1:True
        if request.GET.get('active',None) != None:
            if request.GET.get('active',None) == '1':
                products = products.filter(is_active=True)
                is_failure = PcError.pcBrandProdActiveListEmpty(brand.name)
            elif request.GET.get('active',None) == '0':
                products = products.filter(is_active=False)
                is_failure = PcError.pcBrandProdInActiveListEmpty(brand.name)
        # To check for subgroup filter
        if request.GET.get('sg',None) != None:
            try:
                subgroup = PCModel.ProductSubGroup.objects.get(id=request.GET.get('sg',None))
                products = subgroup.products
            except PCModel.ProductSubGroup.DoesNotExist:
                response_data.update(PcError.pcBrandProdSubGroupListEmpty(brand.name))
                return response_400(response_data)
        # To check for total number of products object
        if products.count() == 0:
                response_data.update(is_failure)
                return response_400(response_data)
        serializer = PCSerializer.ProductListSerializer(products, many=True)
        from_range = 1 if page_num == 1 else ((page_num-1)*15)+1
        to_range = (page_num)*15 if (page_num)*15 < products.count() else products.count()
        response_data.update({
            'pages' : math.ceil(products.count()/15),
            'message' : f'Showing list of {brand.name} products from {from_range} to {to_range} out of {products.count()}',
            'alert' : None if to_range!=products.count() else 'No more products to show',
            'prodList' : serializer.data[(page_num-1)*15: (page_num)*15],
        })
        return response_200(response_data)
    
    '''def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['productId']
        if kwargs['productId'] == str(request.data['id']):
            pass
        try:
            product = PCModel.Product.objects.get(id=kwargs['productId'])
        except PCModel.Product.DoesNotExist:
            failed_response_map['error'] = is_error
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
    
        if product.brand.is_show == True:
            failed_response_map['error'] = product_update_not_applicable
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = PCSerializer.PatchProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            product = PCModel.Product.objects.get(id=kwargs['productId'])
            serializer = PCSerializer.ProductSerializer(product)
            response_map['data'] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''

    '''def destroy(self, request, *args, **kwargs):
        try:
            product = PCModel.Product.objects.get(id=kwargs['productid'])
        except PCModel.Product.DoesNotExist:
            failed_response_map['error'] = is_error
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        
        if product.brand.is_show == True:
            failed_response_map['error'] = product_delete_not_applicable
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)'''


class BrandProdGroupApi(generics.ListAPIView):
    serializer_class = PCSerializer.ProductGroupListSerializer

    def get(self, request, *args, **kwargs):
        response_data = {}
        response_data['brandId'] = kwargs['brandId']
        try:
            brand = PCModel.Brand.objects.get(id=kwargs['brandId'])
        except PCModel.Brand.DoesNotExist:
            response_data.update(PcError.pcBrandNotFound())
            return response_400(response_data)
        
        groups = PCModel.ProductGroup.objects.filter(brand=brand)
        serializer = self.get_serializer(groups, many=True)
        response_data.update({
                "brandName" : brand.name,
                "groupList" : serializer.data,
            })
        return Response(response_data)
