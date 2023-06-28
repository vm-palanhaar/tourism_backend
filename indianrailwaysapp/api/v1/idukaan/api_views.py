from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from userapp import permissions as UserPerm
from indianrailwaysapp import serializers as ShopSerializer
from indianrailwaysapp import models as ShopModel
from indianrailwaysapp.api.v1.idukaan import errors as IrError

from businessapp import models as OrgModel
from businessapp.api import errors as OrgError

from apiutil import errors
from userapp import models as UserModel
from productapp import models as PcModel
from productapp import serializers as PcSerializer



failed_response_map = {'error':None}
response_map = {'data':None}

is_error = 'Something went wrong. Issue reported to Team and your account will be de-activated.'

organization_employee_failed_manager = 'You are not authorized to update organization!'
organization_shop_employee_failed_manager = 'You are not authorized to update shop or access confidential documents!'
organization_shop_employee_failed = 'You are not assocatied to shops!'
organization_shop_employee_add_failed = 'User is not associated with organization!'
organization_shop_employee_add_already_exists_failed = 'User is already associated with shop!'
organization_shop_employee_not_found = 'User is not associated with shop!'
shop_license_already_exist = 'Shop license already exists!'
shop_license_not_found = 'Shop license not available!'
shop_fssai_license_not_found = 'Shop FSSAI license not available!'
shops_list_not_found = 'You are not associated to shops!'
shop_inv_product_listed_stock_page = 'Product is listed under stock page!'
shop_inv_product_listed_out_stock_page = 'Product is listed under out-stock page!'
product_not_found = 'Product is not available!'
shop_inv_list_stock_empty = 'Products are not yet added to shop or out of stock!'
shop_inv_list_out_stock_empty = 'Products are not yet added to shop or in stock!'
shop_inv_not_found = 'Product is already discarded from shop!'
shop_gst_not_found = 'Shop is not associated with GSTIN!'
bad_action = 'Bad action!'

emp_manager = 1
emp_non_manager = 0
emp_not_found = -1
def validate_org_emp(user, org):
    try:
        emp = OrgModel.OrgEmp.objects.get(user=user, org=org)
        if emp.is_manager == True:
            return emp_manager
        return emp_non_manager
    except OrgModel.OrgEmp.DoesNotExist:
        return emp_not_found

def validate_org_shop_emp(user, shop, org):
    org_emp = validate_org_emp(user, org)
    if org_emp == emp_manager:
        return emp_manager
    elif org_emp == emp_non_manager:
        try:
            emp = ShopModel.OrgShopEmp.objects.get(user=user, shop=shop, org=org)
            if emp.is_manager == True:
                return emp_manager
            return emp_non_manager
        except ShopModel.OrgShopEmp.DoesNotExist:
            return emp_not_found
    return emp_not_found
    
def validate_org_shop_emp_return(user, shop, org):
    org_emp = validate_org_emp(user, org)
    if org_emp == emp_manager or org_emp == emp_non_manager:
        try:
            return ShopModel.OrgShopEmp.objects.get(user=user, shop=shop, org=org)
        except ShopModel.OrgShopEmp.DoesNotExist:
            pass
    return None


def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)

def response_200(response_data):
    return Response(response_data, status=status.HTTP_200_OK)

def response_400(response_data):
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

def response_409(response_data):
    return Response(response_data, status=status.HTTP_409_CONFLICT)


class ShopBusinessTypesApi(generics.ListAPIView):
    queryset = ShopModel.ShopBusinessType.objects.all()
    serializer_class = ShopSerializer.ShopBusinessTypeList_iDukaan


class OrgShopApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = str(request.data['org'])
        if kwargs['orgId'] == str(request.data['org']):
            emp = validate_org_emp(request.user, request.data['org'])
            if emp == emp_manager:
                try:
                    ShopModel.ShopLic.objects.get(reg_no = request.data['lic_number'])
                    response_data['error'] = IrError.shop_lic_found
                    return response_409(response_data)
                except ShopModel.ShopLic.DoesNotExist:
                    serializer = ShopSerializer.AddShop_iDukaan(data=request.data, context={'user': request.user})
                    if serializer.is_valid():
                        serializer.save()
                        response_data['irShop'] = serializer.data
                        response_data['message'] = 'Thanks for registering shop with us. We will verify the details provided within 24HRS.'
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    return response_400(serializer.errors)
            elif emp == emp_non_manager:
                response_data['error'] = OrgError.error_business_org_emp_not_mng
                return response_400(response_data)
            response_data['error'] = OrgError.org_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')
        
    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        emp = validate_org_emp(request.user, kwargs['orgId'])
        if emp == emp_manager:
            shop_list = []
            shops = ShopModel.OrgShop.objects.filter(org=kwargs['orgId'])
            if shops.count() != 0:
                for shop in shops:
                    response = ShopSerializer.OrgShopList_iDukaan(shop.shop).data
                    response['org'] = kwargs['orgId']
                    shop_list.append(response)
                response_data['irOrgShops'] = shop_list
                return response_200(response_data)
            response_data['error'] = IrError.org_shop_list_not_found_mng
            return response_400(response_data)
        elif emp == emp_non_manager:
            shop_list = []
            shops = ShopModel.OrgShopEmp.objects.filter(user=request.user, org=kwargs['orgId'])
            if shops.count() != 0:
                for shop in shops:
                    response = ShopSerializer.OrgShopList_iDukaan(shop.shop).data
                    response['org'] = kwargs['orgId']
                    shop_list.append(response)
                response_data['irOrgShops'] = shop_list
                return response_200(response_data)
            response_data['error'] = IrError.org_shop_list_not_found_not_mng
            return response_400(response_data)
        response_data['error'] = OrgError.org_emp_self_not_found
        return response_400(response_data)

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['id']):
            try:
                shop = ShopModel.Shop.objects.get(id=request.data['id'])
            except ShopModel.Shop.DoesNotExist:
                response_data['error'] = IrError.org_shop_not_found
                return response_400(response_data)
            emp = validate_org_shop_emp(request.user, request.data['id'], kwargs['orgId'])
            if emp == emp_manager:
                serializer = ShopSerializer.UpdateShop_iDukaan(shop, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return response_200(response_data)
                return response_400(serializer.errors)
            elif emp == emp_non_manager:
                response_data['error'] = IrError.org_shop_emp_not_mng
                return response_400(response_data)
            response_data['error'] = IrError.org_shop_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')
        
    def retrieve(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['shopId']
        emp = validate_org_shop_emp(request.user, kwargs['shopId'], kwargs['orgId'])
        if emp == emp_manager or emp == emp_non_manager:
            try:
                shop = ShopModel.Shop.objects.get(id=kwargs['shopId'])
                serializer = ShopSerializer.ShopInfo_iDukaan(shop)
                response_data['shop'] = serializer.data
                return response_200(response_data)
            except ShopModel.Shop.DoesNotExist:
                pass 
        response_data['error'] = IrError.org_shop_emp_self_not_found
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ShopListApi(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = ShopSerializer.ShopList_iDukaan
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def get(self, request, *args, **kwargs):
        response_data = {}
        shop_list = []
        shops = ShopModel.OrgShopEmp.objects.filter(user=request.user)
        if shops.count() != 0:
            for shop in shops:
                serializer = self.get_serializer(shop.shop).data
                serializer['org'] = f'{shop.org.id}'
                shop_list.append(serializer)
            response_data['irShops'] = shop_list
            return response_200(response_data)
        
        response_data['error'] = IrError.org_shop_list_not_found
        return response_400(response_data)


class OrgShopEmpAPi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        response_data['orgEmpId'] = str(request.data['empId'])
        if kwargs['shopId'] == str(request.data['shop']):
            org_shop_emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
            if org_shop_emp != None and org_shop_emp.is_manager == True:
                try:
                    org_emp = OrgModel.OrgEmp.objects.get(id=request.data['empId'])
                except OrgModel.OrgEmp.DoesNotExist:
                    response_data['error'] = OrgError.error_business_org_emp_not_found
                    return response_400(response_data)
                try:
                    shop_emp = ShopModel.OrgShopEmp.objects.get(user = org_emp.user, org = org_emp.org, shop = request.data['shop'])
                    IrError.org_shop_add_emp_found['message'] = f'{shop_emp.user.first_name} {shop_emp.user.last_name} is already associated with {shop_emp.shop.name}'
                    response_data['error'] = IrError.org_shop_add_emp_found
                    return response_409(response_data)
                except ShopModel.OrgShopEmp.DoesNotExist:
                    serializer = ShopSerializer.AddOrgShopEmp_iDukaan(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['shopEmp'] = serializer.data
                        response_data['message'] = f'{org_emp.user.first_name} {org_emp.user.last_name} is associated with {org_shop_emp.shop.name}'
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    return response_400(serializer.errors)
            elif org_shop_emp != None and org_shop_emp.is_manager == False:
                    response_data['error'] = IrError.org_shop_emp_not_mng
                    return response_400(response_data)
            response_data['error'] = IrError.org_shop_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        emp = validate_org_shop_emp(request.user, kwargs['shopId'], kwargs['orgId'])
        if emp == emp_manager or emp == emp_non_manager:
            org_shop_emps = ShopModel.OrgShopEmp.objects.filter(org=kwargs['orgId'], shop=kwargs['shopId'])            
            serializer = ShopSerializer.OrgShopEmpList_iDukaan(org_shop_emps, many=True)
            response_data['orgShopEmpList'] = serializer.data
            return response_200(response_data)
        response_data['error'] = IrError.org_shop_emp_self_not_found
        return response_400(response_data)

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['empId']
        response_data['shopId'] = kwargs['shopId']
        if kwargs['empId'] == str(request.data['id']):
            emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
            if emp != None and emp.is_manager == True:
                try:
                    org_shop_emp = ShopModel.OrgShopEmp.objects.get(id=request.data['id'])
                except ShopModel.OrgShopEmp.DoesNotExist:
                    IrError.org_shop_emp_not_found['message'] = IrError.org_shop_emp_not_found['message'].format(emp.shop.name)
                    response_data['error'] = IrError.org_shop_emp_not_found
                    return response_400(response_data)
                if request.user == org_shop_emp.user:
                    IrError.org_shop_emp_self_update['message'] = IrError.org_shop_emp_self_update['message'].format(emp.shop.name)
                    response_data['error'] = IrError.org_shop_emp_self_update
                    return response_400(response_data)
                serializer = ShopSerializer.UpdateOrgShopEmp_iDukaan(org_shop_emp, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return response_200(response_data)
                return response_400(serializer.errors)
            elif emp != None and emp.is_manager == False:
                IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
                response_data['error'] = IrError.org_shop_emp_not_mng
                return response_400(response_data)
            response_data['error'] = IrError.org_shop_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')

    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['empId']
        response_data['shopId'] = kwargs['shopId']
        if kwargs['empId'] == str(request.data['id']):
            emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
            if emp != None and emp.is_manager == True:
                try:
                    org_shop_emp = ShopModel.OrgShopEmp.objects.get(id=kwargs['empId'])
                except ShopModel.OrgShopEmp.DoesNotExist:
                    IrError.org_shop_emp_not_found['message'] = IrError.org_shop_emp_not_found['message'].format(emp.shop.name)
                    response_data['error'] = IrError.org_shop_emp_not_found
                    return response_400(response_data)
                if request.user == org_shop_emp.user:
                    IrError.org_shop_emp_self_delete['message'] = IrError.org_shop_emp_self_delete['message'].format(emp.shop.name)
                    response_data['error'] = IrError.org_shop_emp_self_delete
                    return response_400(response_data)
                org_shop_emp.delete()
                return response_200(response_data)
            elif emp != None and emp.is_manager == False:
                IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
                response_data['error'] = IrError.org_shop_emp_not_mng
                return response_400(response_data)
            response_data['error'] = IrError.org_shop_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')
  

class ShopLicApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['shop']):
            emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
            if emp != None and emp.is_manager == True:
                serializer = ShopSerializer.AddShopLic_iDukaan(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['lic'] = serializer.data
                    response_data['message'] = 'Hello'
                    return Response(response_data, status=status.HTTP_201_CREATED)
                if 'reg_no' in serializer.errors:
                    response_data['error'] = IrError.shop_lic_found
                    return response_409(response_data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif emp != None and emp.is_manager == False:
                IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
                response_data['error'] = IrError.org_shop_emp_not_mng
                return response_400(response_data)
            response_data['error'] = IrError.org_shop_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')
    
    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
        if emp != None and emp.is_manager == True:
            shop_licenses = ShopModel.ShopLic.objects.filter(shop=kwargs['shopId'])
            if shop_licenses.count() != 0:
                serializer = ShopSerializer.ShopLicList_iDukaan(shop_licenses, many=True)
                response_data['licList'] = serializer.data
                return response_200(response_data)
            response_data['error'] = IrError.shop_lic_not_found
            return response_400(response_data)
        elif emp != None and emp.is_manager == False:
            IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
            response_data['error'] = IrError.org_shop_emp_not_mng
            return response_400(response_data)
        response_data['error'] = IrError.org_shop_emp_self_not_found
        return response_400(response_data)


class ShopFssaiLicApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['shop']):
            emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
            if emp != None and emp.is_manager == True:
                serializer = ShopSerializer.AddShopFssaiLic_iDukaan(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['fssaiLic'] = serializer.data
                    response_data['message'] = 'Hello'
                    return Response(response_data, status=status.HTTP_201_CREATED)
                if 'reg_no' in serializer.errors:
                    response_data['error'] = IrError.shop_fssai_lic_found
                    return response_409(response_data)
            elif emp != None and emp.is_manager == False:
                IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
                response_data['error'] = IrError.org_shop_emp_not_mng
                return response_400(response_data)
            response_data['error'] = IrError.org_shop_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')
    
    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
        if emp != None and emp.is_manager == True:
            shop_licenses = ShopModel.ShopFssaiLic.objects.filter(shop=kwargs['shopId'])
            if shop_licenses.count() != 0:
                serializer = ShopSerializer.ShopFssaiLicList_iDukaan(shop_licenses, many=True)
                response_data['fssaiLicList'] = serializer.data
                return response_200(response_data)
            response_data['error'] = IrError.shop_fssai_lic_not_found
            return response_400(response_data)
        elif emp != None and emp.is_manager == False:
            IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
            response_data['error'] = IrError.org_shop_emp_not_mng
            return response_400(response_data)
        response_data['error'] = IrError.org_shop_emp_self_not_found
        return response_400(response_data)


class ShopInvApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['shop']):
            emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
            if emp != None and emp.is_manager == True:
                try:
                    inventory = ShopModel.ShopInv.objects.get(shop=request.data['shop'], product=request.data['product'])
                    if inventory.is_stock:
                        response_data['error'] = IrError.shop_inv_prod_is_found
                        return response_409(response_data)
                    else:
                        response_data['error'] = IrError.shop_inv_prod_os_found
                        return response_409(response_data)
                except ShopModel.ShopInv.DoesNotExist:
                    try:
                        prod = PcModel.Product.objects.get(id=request.data['product'])
                    except PcModel.Product.DoesNotExist:
                        response_data['error'] = ''
                        return response_400(product_not_found)
                    serializer = ShopSerializer.AddShopInv_iDukaan(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['invProd'] = serializer.data
                        if prod.brand.is_show:
                            response_data['message'] = f'{prod.brand.name} {prod.name} is now available at {emp.shop.name}'
                        else:
                            response_data['message'] = f'{prod.brand}'
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif emp != None and emp.is_manager == False:
                IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
                response_data['error'] = IrError.org_shop_emp_not_mng
                return response_400(response_data)
            response_data['error'] = IrError.org_shop_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        emp = validate_org_shop_emp(request.user, kwargs['shopId'], kwargs['orgId'])
        if emp == emp_manager or emp == emp_non_manager:
            if request.GET.get('q',None) == 'is':
                stock = True
            elif request.GET.get('q',None) == 'os':
                stock = False
            else:
               return errors.response_401_block_user(request=request,reason='') 
            inv_prods = ShopModel.ShopInv.objects.filter(shop = kwargs['shopId'], is_stock=stock)
            if inv_prods.count() == 0:
                if stock:
                    response_data['error'] = IrError.shop_inv_in_stock_not_found
                    return response_400(response_data)
                response_data['error'] = IrError.shop_inv_out_stock_not_found
                return response_400(response_data)
            serializer = ShopSerializer.ShopInvList(inv_prods, many=True)
            response_data['invList'] = serializer.data
            return response_200(response_data)
        response_data['error'] = IrError.org_shop_emp_self_not_found
        return response_400(response_data)

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = str(request.data['id'])
        response_data['shopId'] = kwargs['shopId']
        emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
        if emp != None and emp.is_manager == True:
            try:
                inv = ShopModel.ShopInv.objects.get(id=request.data['id'])
            except ShopModel.ShopInv.DoesNotExist:
                response_data['error'] = ''
                return response_400(shop_inv_not_found)
            serializer = ShopSerializer.PatchShopInv_iDukaan(inv, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response_200(response_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif emp != None and emp.is_manager == False:
            IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
            response_data['error'] = IrError.org_shop_emp_not_mng
            return response_400(response_data)
        response_data['error'] = IrError.org_shop_emp_self_not_found
        return response_400(response_data)
    
    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = str(request.data['id'])
        response_data['shopId'] = kwargs['shopId']
        emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
        if emp != None and emp.is_manager == True:
            try:
                ShopModel.ShopInv.objects.get(id=request.data['id']).delete()
                return response_200(response_data)
            except ShopModel.ShopInv.DoesNotExist:
                response_data['error'] = ''
                return error_response(shop_inv_not_found)
        elif emp != None and emp.is_manager == False:
            IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
            response_data['error'] = IrError.org_shop_emp_not_mng
            return response_400(response_data)
        response_data['error'] = IrError.org_shop_emp_self_not_found
        return response_400(response_data)


class ShopGstPostGetAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['shop']):
            emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
            if emp != None and emp.is_manager == True:
                try:
                    shopGst = ShopModel.ShopGst.objects.get(gst = request.data['gst'], shop = request.data['shop'])
                    IrError.shop_gst_found['message'] = IrError.shop_gst_found['message'].format(shopGst.gst.gstin)
                    response_data['error'] = IrError.shop_gst_found
                    return response_409(response_data)
                except ShopModel.ShopGst.DoesNotExist:
                    try:
                        OrgModel.OrgStateGstOps.objects.get(id=request.data['gst'])
                    except OrgModel.OrgStateGstOps.DoesNotExist:
                        response_data['error'] = OrgError.error_business_org_ops_not_found
                        return response_409(response_data)
                    serializer = ShopSerializer.AddShopGst_iDukaan(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['shopGst'] = serializer.data
                        response_data['message'] = 'Success, GSTIN connected to shop!'
                        return Response(response_data, status=status.HTTP_201_CREATED)
            elif emp != None and emp.is_manager == False:
                IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
                response_data['error'] = IrError.org_shop_emp_not_mng
                return response_400(response_data)
            response_data['error'] = IrError.org_shop_emp_self_not_found
            return response_400(response_data)
        return errors.response_401_block_user(request=request,reason='')

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        emp = validate_org_shop_emp_return(request.user, kwargs['shopId'], kwargs['orgId'])
        if emp != None and emp.is_manager == True:
            gst = ShopModel.ShopGst.objects.filter(org=kwargs['orgId'], shop=kwargs['shopId'])
            if gst.count() > 0:
                serializer = ShopSerializer.ShopGstList_iDukaan(gst, many=True)
                response_data['gstList'] = serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            response_data['error'] = IrError.shop_gst_not_found
            return response_400(response_data)
        if emp != None and emp.is_manager == False:
                IrError.org_shop_emp_not_mng['message'] = IrError.org_shop_emp_not_mng['message'].format(emp.shop.name)
                response_data['error'] = IrError.org_shop_emp_not_mng
                return response_400(response_data)
        response_data['error'] = IrError.org_shop_emp_self_not_found
        return response_400(response_data)
