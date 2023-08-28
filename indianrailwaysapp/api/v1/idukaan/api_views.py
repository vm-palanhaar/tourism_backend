from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from userapp import permissions as UserPerm
from indianrailwaysapp import serializers as ShopSerializer
from indianrailwaysapp import models as ShopModel
from indianrailwaysapp.api.v1.idukaan import errors as IrError

from businessapp import models as OrgModel
from businessapp.api import errors as OrgError

from apiutil import errors as UtilError
from productapp import models as PcModel

product_not_found = 'Product is not available!'

def validateOrgEmpObj(user, org):
    try:
        return OrgModel.OrgEmp.objects.get(user=user, org=org)
    except OrgModel.OrgEmp.DoesNotExist:
        return None

def validateOrgShopEmpMap_Shop_IsMng(user, shop, org):
    orgEmp = validateOrgEmpObj(user, org)
    if orgEmp != None and orgEmp.is_manager == True:
        try:
            return {
                'shop' : ShopModel.Shop.objects.get(id = shop),
                'emp' : orgEmp,
                'isMng' : orgEmp.is_manager
            }
        except ShopModel.Shop.DoesNotExist:
            return {
                'shop': None,
                'emp' : orgEmp,
                'isMng' : orgEmp.is_manager
            }
    elif orgEmp != None and orgEmp.is_manager == False:
        try:
            orgShopEmp = ShopModel.OrgShopEmp.objects.get(user=user, shop=shop, org=org)
            return {
                'shop' : orgShopEmp.shop,
                'emp' : orgShopEmp,
                'isMng' : orgShopEmp.is_manager
            }
        except ShopModel.OrgShopEmp.DoesNotExist:
            return {
                'shop' : None,
                'emp' : orgEmp,
                'isMng' : orgEmp.is_manager
            }
    return None


def response_200(response_data):
    return Response(response_data, status=status.HTTP_200_OK)

def response_400(response_data):
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

def response_401(response_data):
    return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

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
            org_emp = validateOrgEmpObj(request.user, request.data['org'])
            if org_emp != None and org_emp.org.is_active == True:
                if org_emp.is_manager == True:
                    try:
                        ShopModel.ShopLic.objects.get(reg_no = request.data['lic_number'])
                        response_data.update(IrError.irShopLicFound())
                        return response_409(response_data)
                    except ShopModel.ShopLic.DoesNotExist:
                        serializer = ShopSerializer.AddShop_iDukaan(data=request.data, context={'user': request.user})
                        if serializer.is_valid():
                            serializer.save()
                            response_data['irShop'] = serializer.data
                            response_data['message'] = 'Thanks for registering shop with us. We will verify the details provided within 24HRS.'
                            return Response(response_data, status=status.HTTP_201_CREATED)
                    response_data.update(UtilError.bodyEmptyFields())
                    return response_400(response_data)
                elif org_emp.is_manager == False:
                    response_data.update(OrgError.businessOrgEmpNotMng(org_emp.org.name))
                    return response_400(response_data)
            elif org_emp != None and org_emp.org.is_active == False:
                response_data.update(OrgError.businessOrgNotVerified(org_emp.org.name))
                return response_400(response_data)
            response_data.update(OrgError.businessOrgEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrOrgShopApiCreate_OrgId_Url-{0}_HB-{1}'.format(kwargs['orgId'],request.data['org'])))
        return response_401(response_data)
        
    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
        if org_emp != None and org_emp.is_manager == True:
            shop_list = []
            shops = ShopModel.OrgShop.objects.filter(org=kwargs['orgId'])
            if shops.count() != 0:
                for shop in shops:
                    response = ShopSerializer.OrgShopList_iDukaan(shop.shop).data
                    response['org'] = kwargs['orgId']
                    shop_list.append(response)
                response_data['irOrgShops'] = shop_list
                return response_200(response_data)
            response_data.update(IrError.irOrgShopListEmptyMng())
            return response_400(response_data)
        elif org_emp != None and org_emp.is_manager == False:
            shop_list = []
            shops = ShopModel.OrgShopEmp.objects.filter(user=request.user, org=kwargs['orgId'])
            if shops.count() != 0:
                for shop in shops:
                    response = ShopSerializer.OrgShopList_iDukaan(shop.shop).data
                    response['org'] = kwargs['orgId']
                    shop_list.append(response)
                response_data['irOrgShops'] = shop_list
                return response_200(response_data)
            response_data.update(IrError.irOrgShopListEmptyNotMng())
            return response_400(response_data)
        response_data.update(OrgError.businessOrgEmpSelfNotFound())
        return response_400(response_data)

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['id']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, request.data['id'], kwargs['orgId'])
            if orgShopEmp != None:
                if orgShopEmp['shop'] != None and orgShopEmp['isMng'] == True:
                    serializer = ShopSerializer.UpdateShop_iDukaan(orgShopEmp['shop'], data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return response_200(response_data)
                    response_data.update(UtilError.bodyEmptyFields())
                    return response_400(response_data)
                elif orgShopEmp['shop'] != None and orgShopEmp['isMng'] == False:
                    response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                    return response_400(response_data)
                elif orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                    response_data.update(IrError.irOrgShopNotFound())
                    return response_400(response_data)
                elif orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
                    response_data.update(IrError.irOrgShopEmpSelfNotFound())
                    return response_400(response_data)
            response_data.update(IrError.irOrgShopEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrOrgShopApiPatch_ShopId_Url-{0}_HB-{1}'.format(kwargs['shopId'],request.data['id'])))
        return response_401(response_data)
            
    def retrieve(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['shopId']
        orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
        if orgShopEmp != None and orgShopEmp['shop'] != None:
            serializer = ShopSerializer.ShopInfo_iDukaan(orgShopEmp['shop'])
            response_data['shop'] = serializer.data
            return response_200(response_data)
        response_data.update(IrError.irOrgShopEmpSelfNotFound())
        return response_400(response_data)


class ShopListApi(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = ShopSerializer.ShopList_iDukaan
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def get(self, request, *args, **kwargs):
        shops = ShopModel.OrgShopEmp.objects.filter(user=request.user)
        if shops.count() != 0:
            response_data = {}
            shop_list = []
            for shop in shops:
                serializer = self.get_serializer(shop.shop).data
                serializer['org'] = f'{shop.org.id}'
                shop_list.append(serializer)
            response_data['irShops'] = shop_list
            return response_200(response_data)
        return response_400(IrError.irOrgShopListEmpty())


class OrgShopEmpAPi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        response_data['orgEmpId'] = str(request.data['empId'])
        if kwargs['shopId'] == str(request.data['shop']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None:
                if orgShopEmp['shop'] != None and orgShopEmp['shop'].is_active == True and orgShopEmp['shop'].is_verified == True:
                    if orgShopEmp['isMng'] == True:
                        try:
                            orgEmp = OrgModel.OrgEmp.objects.get(id = request.data['empId'])
                            try:
                                shopEmp = ShopModel.OrgShopEmp.objects.get(user = orgEmp.user, org = orgEmp.org, shop = request.data['shop'])
                                response_data.update(IrError.irOrgShopAddEmpFound(shopEmp))
                                return response_409(response_data)
                            except ShopModel.OrgShopEmp.DoesNotExist:
                                pass
                        except OrgModel.OrgEmp.DoesNotExist:
                            response_data.update(OrgError.businessOrgEmpNotFound(orgShopEmp.org.name))
                            return response_400(response_data)
                        serializer = ShopSerializer.AddOrgShopEmp_iDukaan(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            response_data['shopEmp'] = serializer.data
                            response_data['message'] = '{0} {1} is associated with {2}'.format(orgEmp.user.first_name, orgEmp.user.last_name, orgShopEmp['shop'].name)
                            return Response(response_data, status=status.HTTP_201_CREATED)
                        response_data.update(UtilError.bodyEmptyFields())
                        return response_400(response_data)
                    elif orgShopEmp['isMng'] == False:
                        response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                        return response_400(response_data)
                elif orgShopEmp['shop'] != None and orgShopEmp['shop'].is_active == True and orgShopEmp['shop'].is_verified == False:
                    response_data.update(IrError.irOrgShopNotVerified(orgShopEmp['shop'].name))
                    return response_400(response_data)
                elif orgShopEmp['shop'] != None and orgShopEmp['shop'].is_active == False and orgShopEmp['shop'].is_verified == True:
                    response_data.update(IrError.irOrgShopInActive(orgShopEmp['shop'].name))
                    return response_400(response_data)
                elif orgShopEmp['shop'] != None and orgShopEmp['shop'].is_active == False and orgShopEmp['shop'].is_verified == False:
                    response_data.update(IrError.irOrgShopInActiveNotVerified(orgShopEmp['shop'].name))
                    return response_400(response_data)
                elif orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                    response_data.update(IrError.irOrgShopNotFound())
                    return response_400(response_data)
            response_data.update(IrError.irOrgShopEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrOrgShopEmpApiCreate_ShopId_Url-{0}_HB-{1}'.format(kwargs['shopId'],request.data['shop'])))
        return response_401(response_data)
    
    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
        if orgShopEmp != None and orgShopEmp['shop'] != None:
            shopEmps = ShopModel.OrgShopEmp.objects.filter(org=kwargs['orgId'], shop=kwargs['shopId'])            
            serializer = ShopSerializer.OrgShopEmpList_iDukaan(shopEmps, many=True)
            response_data['orgShopEmpList'] = serializer.data
            return response_200(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
            response_data.update(IrError.irOrgShopNotFound())
            return response_400(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
            pass
        response_data.update(IrError.irOrgShopEmpSelfNotFound())
        return response_400(response_data)
            
    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['empId']
        response_data['shopId'] = kwargs['shopId']
        if kwargs['empId'] == str(request.data['id']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None and orgShopEmp['shop'] != None:
                if orgShopEmp['isMng'] == True:
                    try:
                        shopEmp = ShopModel.OrgShopEmp.objects.get(id=request.data['id'])
                    except ShopModel.OrgShopEmp.DoesNotExist:
                        response_data.update(IrError.irOrgShopEmpNotFound(request.data['name'], orgShopEmp['shop'].name))
                        return response_400(response_data)
                    if request.user == shopEmp.user:
                        response_data.update(IrError.irOrgShopEmpSelfUd(orgShopEmp['shop'].name))
                        return response_400(response_data)
                    serializer = ShopSerializer.UpdateOrgShopEmp_iDukaan(shopEmp, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return response_200(response_data)
                    response_data.update(UtilError.bodyEmptyFields())
                    return response_400(response_data)
                elif orgShopEmp['isMng'] == False:
                        response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                        return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                response_data.update(IrError.irOrgShopNotFound())
                return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrOrgShopEmpApiPartial_EmpId_Url-{0}_HB-{1}'.format(kwargs['empId'],request.data['id'])))
        return response_401(response_data)

    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['empId']
        response_data['shopId'] = kwargs['shopId']
        if kwargs['empId'] == str(request.data['id']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None and orgShopEmp['shop'] != None:
                if orgShopEmp['isMng'] == True:
                    try:
                        shopEmp = ShopModel.OrgShopEmp.objects.get(id=request.data['id'])
                    except ShopModel.OrgShopEmp.DoesNotExist:
                        response_data.update(IrError.irOrgShopEmpNotFound(request.data['name'], orgShopEmp['shop'].name))
                        return response_400(response_data)
                    if request.user == shopEmp.user:
                        response_data.update(IrError.irOrgShopEmpSelfUd(orgShopEmp['shop'].name))
                        return response_400(response_data)
                    shopEmp.delete()
                    return response_200(response_data)
                elif orgShopEmp['isMng'] == False:
                    response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                    return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                response_data.update(IrError.irOrgShopNotFound())
                return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrOrgShopEmpApiDelete_EmpId_Url-{0}_HB-{1}'.format(kwargs['empId'],request.data['id'])))
        return response_401(response_data)


class ShopLicApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['shop']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None and orgShopEmp['shop'] != None:
                if orgShopEmp['isMng'] == True:
                    serializer = ShopSerializer.AddShopLic_iDukaan(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['lic'] = serializer.data
                        response_data['message'] = 'Hello'
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    if 'reg_no' in serializer.errors and 'shop' not in serializer.errors:
                        response_data.update(IrError.irShopLicFound())
                        return response_409(response_data)
                    response_data.update(UtilError.bodyEmptyFields())
                    return response_400(response_data)
                elif orgShopEmp['isMng'] == False:
                    response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                    return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                response_data.update(IrError.irOrgShopNotFound())
                return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrShopLicApiCreate_ShopId_Url-{0}_HB-{1}'.format(kwargs['shopId'],request.data['shop'])))
        return response_401(response_data)
    
    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
        if orgShopEmp != None and orgShopEmp['shop'] != None:
            if orgShopEmp['isMng'] == True:
                lics = ShopModel.ShopLic.objects.filter(shop=kwargs['shopId'])
                if lics.count() != 0:
                    serializer = ShopSerializer.ShopLicList_iDukaan(lics, many=True)
                    response_data['licList'] = serializer.data
                    return response_200(response_data)
                response_data.update(IrError.irShopLicNotFound())
                return response_400(response_data)
            elif orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                return response_400(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
            response_data.update(IrError.irOrgShopNotFound())
            return response_400(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
            response_data.update(IrError.irOrgShopEmpSelfNotFound())
            return response_400(response_data)


class ShopFssaiLicApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['shop']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None and orgShopEmp['shop'] != None:
                if orgShopEmp['isMng'] == True:
                    serializer = ShopSerializer.AddShopFssaiLic_iDukaan(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['fssaiLic'] = serializer.data
                        response_data['message'] = 'Hello'
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    if 'reg_no' in serializer.errors:
                        response_data.update(IrError.irShopFssaiLicFound())
                        return response_409(response_data)
                    response_data.update(UtilError.bodyEmptyFields())
                    return response_400(response_data)
                elif orgShopEmp['isMng'] == False:
                    response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                    return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                response_data.update(IrError.irOrgShopNotFound())
                return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrShopFssaiLicApiCreate_ShopId_Url-{0}_HB-{1}'.format(kwargs['shopId'],request.data['shop'])))
        return response_401(response_data)
    
    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
        if orgShopEmp != None and orgShopEmp['shop'] != None:
            lics = ShopModel.ShopFssaiLic.objects.filter(shop=kwargs['shopId'])
            if lics.count() != 0:
                serializer = ShopSerializer.ShopFssaiLicList_iDukaan(lics, many=True)
                response_data['fssaiLicList'] = serializer.data
                return response_200(response_data)
            if orgShopEmp['isMng'] == True:
                response_data.update(IrError.irShopFssaiLicNotFoundEmpMng())
                return response_400(response_data)
            elif orgShopEmp['isMng'] == False:
                response_data.update(IrError.irShopFssaiLicNotFoundEmpNonMng(orgShopEmp['shop'].name))
                return response_400(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
            response_data.update(IrError.irOrgShopNotFound())
            return response_400(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
            response_data.update(IrError.irOrgShopEmpSelfNotFound())
            return response_400(response_data)


class ShopInvApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['shop']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None:
                if orgShopEmp['shop'] != None and orgShopEmp['shop'].is_active == True and orgShopEmp['shop'].is_verified == True:
                    if orgShopEmp['isMng'] == True:
                        try:
                            inv = ShopModel.ShopInv.objects.get(shop=request.data['shop'], product=request.data['product'])
                            if inv.is_stock:
                                response_data.update(IrError.irShopInvProdIsFound())
                                return response_409(response_data)
                            response_data.update(IrError.irShopInvProdOsFound())
                            return response_409(response_data)
                        except ShopModel.ShopInv.DoesNotExist:
                            try:
                                prod = PcModel.Prod.objects.get(id=request.data['product'])
                            except PcModel.Prod.DoesNotExist:
                                response_data.update(product_not_found)
                                return response_400(response_data)
                            serializer = ShopSerializer.AddShopInv_iDukaan(data=request.data)
                            if serializer.is_valid():
                                serializer.save()
                                response_data['invProd'] = serializer.data
                                if prod.brand.is_show:
                                    response_data['message'] = '{0} {1} is now available at {2}'.format(prod.brand.name, prod.name, orgShopEmp['shop'].name)
                                else:
                                    response_data['message'] = '{0} is now available at {1}'.format( prod.name, orgShopEmp['shop'].name)
                                return Response(response_data, status=status.HTTP_201_CREATED)
                            response_data.update(UtilError.bodyEmptyFields())
                            return response_400(response_data)
                    elif orgShopEmp['isMng'] == False:
                        response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                        return response_400(response_data)
                elif orgShopEmp['shop'] != None and orgShopEmp['shop'].is_active == True and orgShopEmp['shop'].is_verified == False:
                    response_data.update(IrError.irOrgShopNotVerified(orgShopEmp['shop'].name))
                    return response_400(response_data)
                elif orgShopEmp['shop'] != None and orgShopEmp['shop'].is_active == False and orgShopEmp['shop'].is_verified == True:
                    response_data.update(IrError.irOrgShopInActive(orgShopEmp['shop'].name))
                    return response_400(response_data)
                elif orgShopEmp['shop'] != None and orgShopEmp['shop'].is_active == False and orgShopEmp['shop'].is_verified == False:
                    response_data.update(IrError.irOrgShopInActiveNotVerified(orgShopEmp['shop'].name))
                    return response_400(response_data)
                elif orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                    response_data.update(IrError.irOrgShopNotFound())
                    return response_400(response_data)
            response_data.update(IrError.irOrgShopEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrShopInvApiCreate_ShopId_Url-{0}_HB-{1}'.format(kwargs['shopId'],request.data['shop']))) 
        return response_401(response_data)

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
        if orgShopEmp != None and orgShopEmp['shop'] != None:
            if orgShopEmp['isMng'] == True or orgShopEmp['isMng'] == False:
                if request.GET.get('q',None) == 'is':
                    stock = True
                elif request.GET.get('q',None) == 'os':
                    stock = False
                else:
                    response_data.update(UtilError.badActionUser(request, 'IrShopInvApiList_ShopId_Url-{0}'.format(kwargs['shopId'])))
                    return response_401(response_data)
                prods = ShopModel.ShopInv.objects.filter(shop = kwargs['shopId'], is_stock=stock)
                if prods.count() == 0:
                    if stock:
                        response_data.update(IrError.irShopInvIsNotFound())
                        return response_400(response_data)
                    response_data.update(IrError.irShopInvOsNotFound())
                    return response_400(response_data)
                serializer = ShopSerializer.ShopInvList(prods, many=True)
                response_data['invList'] = serializer.data
                return response_200(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
            response_data.update(IrError.irOrgShopNotFound())
            return response_400(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
            response_data.update(IrError.irOrgShopEmpSelfNotFound())
            return response_400(response_data)

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = str(request.data['id'])
        response_data['shopId'] = kwargs['shopId']
        if kwargs['invId'] == str(request.data['id']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None and orgShopEmp['shop'] != None:
                if orgShopEmp['isMng'] == True:
                    try:
                        inv = ShopModel.ShopInv.objects.get(id=request.data['id'])
                    except ShopModel.ShopInv.DoesNotExist:
                        response_data.update(IrError.irShopInvNotFound(orgShopEmp['shop'].name))
                        return response_400(response_data)
                    serializer = ShopSerializer.PatchShopInv_iDukaan(inv, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return response_200(response_data)
                    response_data.update(UtilError.bodyEmptyFields())
                    return response_400(response_data)
                elif orgShopEmp['isMng'] == False:
                    response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                    return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                response_data.update(IrError.irOrgShopNotFound())
                return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrShopInvApiPatch_InvId_Url-{0}_HB-{1}'.format(kwargs['invId'],request.data['id'])))   
        return response_401(response_data)
    
    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = str(request.data['id'])
        response_data['shopId'] = kwargs['shopId']
        if kwargs['invId'] == str(request.data['id']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None and orgShopEmp['shop'] != None:
                    if orgShopEmp['isMng'] == True:
                        try:
                            ShopModel.ShopInv.objects.get(id=request.data['id']).delete()
                            return response_200(response_data)
                        except ShopModel.ShopInv.DoesNotExist:
                            response_data.update(IrError.irShopInvNotFound(orgShopEmp['shop'].name))
                            return response_400(response_data)
                    elif orgShopEmp['isMng'] == False:
                        response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                        return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                response_data.update(IrError.irOrgShopNotFound())
                return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpSelfNotFound())
                return response_400(response_data) 
        response_data.update(UtilError.badActionUser(request, 'IrShopInvApiDelete_InvId_Url-{0}_HB-{1}'.format(kwargs['invId'],request.data['id'])))
        return response_401(response_data)


class ShopGstApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['shop']):
            orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
            if orgShopEmp != None and orgShopEmp['shop'] != None:
                if orgShopEmp['isMng'] == True:
                    try:
                        shopGst = ShopModel.ShopGst.objects.get(gst = request.data['gst'], shop = request.data['shop'])
                        response_data.update(IrError.irShopGstFound(orgShopEmp['shop'].name, shopGst.gst.gstin))
                        return response_409(response_data)
                    except ShopModel.ShopGst.DoesNotExist:
                        try:
                            OrgModel.OrgStateGstOps.objects.get(id=request.data['gst'])
                        except OrgModel.OrgStateGstOps.DoesNotExist:
                            response_data.update(OrgError.businessOrgOpsNotFound())
                            return response_409(response_data)
                        serializer = ShopSerializer.AddShopGst_iDukaan(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            response_data['shopGst'] = serializer.data
                            response_data['message'] = 'Success, GSTIN connected to shop!'
                            return Response(response_data, status=status.HTTP_201_CREATED)
                        response_data.update(UtilError.bodyEmptyFields())
                        return response_400(response_data)
                elif orgShopEmp['isMng'] == False:
                    response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                    return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
                response_data.update(IrError.irOrgShopNotFound())
                return response_400(response_data)
            elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'IrShopGstApiCreate_ShopId_Url-{0}_HB-{1}'.format(kwargs['shopId'],request.data['shop'])))  
        return response_401(response_data)

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        orgShopEmp = validateOrgShopEmpMap_Shop_IsMng(request.user, kwargs['shopId'], kwargs['orgId'])
        if orgShopEmp != None and orgShopEmp['shop'] != None:
            if orgShopEmp['isMng'] == True:
                gst = ShopModel.ShopGst.objects.filter(org=kwargs['orgId'], shop=kwargs['shopId'])
                if gst.count() > 0:
                    serializer = ShopSerializer.ShopGstList_iDukaan(gst, many=True)
                    response_data['gstList'] = serializer.data
                    return response_200(response_data)
                response_data.update(IrError.irShopGstNotFound(orgShopEmp['shop'].name))
                return response_400(response_data)
            elif orgShopEmp['isMng'] == False:
                response_data.update(IrError.irOrgShopEmpNotMng(orgShopEmp['shop'].name))
                return response_400(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == True:
            response_data.update(IrError.irOrgShopNotFound())
            return response_400(response_data)
        elif orgShopEmp != None and orgShopEmp['shop'] == None and orgShopEmp['isMng'] == False:
            response_data.update(IrError.irOrgShopEmpSelfNotFound())
            return response_400(response_data)
