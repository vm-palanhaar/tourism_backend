from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from userapp import permissions as UserPerm
from indianrailwaysapp import serializers as ShopSerializer
from indianrailwaysapp import models as ShopModel
from businessapp import models as OrgModel
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
        emp = OrgModel.OrganizationEmployee.objects.get(user=user, organization=org)
        if emp.manager == True:
            return emp_manager
        return emp_non_manager
    except OrgModel.OrganizationEmployee.DoesNotExist:
        return emp_not_found
    

def validate_org_shop_emp(user, shop, org):
    org_emp = validate_org_emp(user, org)
    if org_emp == emp_manager:
        return emp_manager
    elif org_emp == emp_non_manager:
        try:
            emp = ShopModel.OrganizationShopEmployee.objects.get(user=user, shop=shop, organization=org)
            if emp.is_manager == True:
                return emp_manager
            return emp_non_manager
        except OrgModel.OrganizationEmployee.DoesNotExist:
            return emp_not_found
    return emp_not_found
    

def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


class ShopBusinessTypeListAPIView(generics.ListAPIView):
    queryset = ShopModel.ShopBusinessType.objects.all()
    serializer_class = ShopSerializer.ShopBusinessTypeListSerializer_iDukaan


class AddShopAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    serializer_class = ShopSerializer.AddShopSerializer_iDukaan
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def post(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, request.data['organization'])
        if check == emp_manager:
            try:
                shop_lic = ShopModel.ShopLicense.objects.get(registration = request.data['lic_number'])
                failed_response_map['error'] = shop_license_already_exist
                return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
            except ShopModel.ShopLicense.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif check == emp_non_manager:
            failed_response_map['error'] = organization_employee_failed_manager
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)

        else:
            failed_response_map['error'] = is_error
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        

class ShopListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = ShopSerializer.ShopListSerializer_iDukaan
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def get(self, request, *args, **kwargs):
        shop_list = []
        shops = ShopModel.OrganizationShopEmployee.objects.filter(user=request.user)
        if shops.count() != 0:
            for shop in shops:
                serializer = self.get_serializer(shop.shop).data
                serializer['org'] = f'{shop.organization.id}'
                shop_list.append(serializer)
            response_map['data'] = shop_list
            return Response(response_map, status=status.HTTP_200_OK)
        
        failed_response_map['error'] = shops_list_not_found
        return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


class OrgShopListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = ShopSerializer.OrganizationShopListSerializer_iDukaan
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def get(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, kwargs['orgid'])
        if check == emp_manager:
            shop_list = []
            shops = ShopModel.OrganizationShop.objects.filter(organization=kwargs['orgid'])
            if shops.count() != 0:
                for shop in shops:
                    response = self.get_serializer(shop.shop).data
                    response['org'] = kwargs['orgid']
                    shop_list.append(response)
                response_map['data'] = shop_list
                return Response(response_map, status=status.HTTP_200_OK)
            failed_response_map['error'] = organization_shop_employee_failed
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)  
        
        elif check == emp_non_manager:
            shop_list = []
            shops = ShopModel.OrganizationShopEmployee.objects\
                    .filter(user=request.user, organization=kwargs['orgid'])
            if shops.count() != 0:
                for shop in shops:
                    response = self.get_serializer(shop.shop).data
                    response['org'] = kwargs['orgid']
                    shop_list.append(response)
                response_map['data'] = shop_list
                return Response(response_map, status=status.HTTP_200_OK)
            failed_response_map['error'] = organization_shop_employee_failed
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            failed_response_map['error'] = is_error
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


class OrgshopPatchDetailsAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def partial_update(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            try:
                shop = ShopModel.Shop.objects.get(id=request.data['id'])
            except ShopModel.Shop.DoesNotExist:
                failed_response_map['error'] = is_error
                return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
            serializer = ShopSerializer.PatchShopSerializer_iDukaan(shop, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif check == emp_non_manager:
            failed_response_map['error'] = organization_shop_employee_failed_manager
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)

        else:
            failed_response_map['error'] = is_error
            return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        
    
    def retrieve(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager or check == emp_non_manager:
            shop = ShopModel.Shop.objects.get(pk=kwargs['shopid'])
            serializer = ShopSerializer.ShopDetailsSerializer_iDukaan(shop)
            response_map['data'] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)
        
        failed_response_map['error'] = is_error
        return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


class AddOrgShopEmpAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    serializer_class = ShopSerializer.AddOrgShopEmpSerializer_iDukaan
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def post(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            try:
                employee = OrgModel.OrganizationEmployee.objects.get(id=request.data['empid'])
            except OrgModel.OrganizationEmployee.DoesNotExist:
                failed_response_map['error'] = organization_shop_employee_add_failed
                return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                ShopModel.OrganizationShopEmployee.objects.get(user=employee.user,
                    organization=employee.organization, shop=request.data['shop'])
                failed_response_map['error'] = organization_shop_employee_add_already_exists_failed
                return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
            except ShopModel.OrganizationShopEmployee.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)


class OrgShopEmpListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def get(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager or check == emp_non_manager:
            org_shop_emps = ShopModel.OrganizationShopEmployee.objects.filter(organization=kwargs['orgid'], shop=kwargs['shopid'])            
            serializer = ShopSerializer.OrgShopEmpListSerializer_iDukaan(org_shop_emps, many=True)
            response_map['data'] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)

        return error_response(is_error)
        

class OrgShopEmpPatchDeleteAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def partial_update(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            try:
                org_shop_emp = ShopModel.OrganizationShopEmployee.objects.get(id=request.data['id'])
            except ShopModel.OrganizationShopEmployee.DoesNotExist:
                return error_response(organization_shop_employee_not_found)
            
            serializer = ShopSerializer.UpdateOrgShopEmpSerializer_iDukaan(org_shop_emp, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)


    def destroy(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            try:
                org_shop_emp = ShopModel.OrganizationShopEmployee.objects.get(id=kwargs['empid'])
                if request.user == org_shop_emp.user:
                    return error_response(bad_action)
                org_shop_emp.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ShopModel.OrganizationShopEmployee.DoesNotExist:
                return error_response(organization_shop_employee_not_found)            

        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)
    

class ShopLicenseAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            serializer = ShopSerializer.AddShopLicenseSerializer_iDukaan(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)
    
    def list(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            shop_licenses = ShopModel.ShopLicense.objects.filter(shop=kwargs['shopid'])
            if shop_licenses.count() != 0:
                serializer = ShopSerializer.ShopLicenseSerializer_iDukaan(shop_licenses, many=True)
                response_map['data'] = serializer.data
                return Response(response_map, status=status.HTTP_200_OK)
            else:
                return error_response(shop_license_not_found)
            
        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)


class ShopFssaiLicenseAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            serializer = ShopSerializer.AddShopFssaiLicenseSerializer_iDukaan(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)
    
    def list(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            shop_licenses = ShopModel.ShopFssaiLicense.objects.filter(shop=kwargs['shopid'])
            if shop_licenses.count() != 0:
                serializer = ShopSerializer.ShopFssaiLicenseSerializer_iDukaan(shop_licenses, many=True)
                response_map['data'] = serializer.data
                return Response(response_map, status=status.HTTP_200_OK)
            else:
                return error_response(shop_fssai_license_not_found)
            
        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)


class AddShopInventoryAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    serializer_class = ShopSerializer.AddShopInventorySerializer_iDukaan
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def post(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            try:
                inventory = ShopModel.ShopInventory.objects.get(shop=request.data['shop'], product=request.data['product'])
                if inventory.is_stock:
                    return error_response(shop_inv_product_listed_stock_page)
                else:
                    return error_response(shop_inv_product_listed_out_stock_page)
            except ShopModel.ShopInventory.DoesNotExist:
                pass

            try:
                product = PcModel.Product.objects.get(id=request.data['product'])
            except PcModel.Product.DoesNotExist:
                return error_response(product_not_found)
            
            # if product.is_active == False and product.brand.is_show == True:
            #     return error_response(product_not_found)
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)


class ShopInventoryListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = ShopSerializer.ShopInventoryListSerializer
    permission_classes = [IsAuthenticated,UserPerm.IsVerified] 

    def get(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager or check == emp_non_manager:
            if request.GET.get('q',None) == '1':
                stock = True
            elif request.GET.get('q',None) == '0':
                stock = False
            else:
               return error_response(is_error)  

            inv_prods = ShopModel.ShopInventory.objects.filter(shop = kwargs['shopid'], is_stock=stock)
            if inv_prods.count() == 0:
                if stock:
                    return error_response(shop_inv_list_stock_empty)
                return error_response(shop_inv_list_out_stock_empty)
            
            serializer = self.get_serializer(inv_prods, many=True)
            response_map['data'] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)
            
        return error_response(is_error)


class ShopInventoryPatchDeleteAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def partial_update(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            try:
                inv = ShopModel.ShopInventory.objects.get(id=request.data['id'])
            except ShopModel.ShopInventory.DoesNotExist:
                return error_response(shop_inv_not_found)
            
            serializer = ShopSerializer.PatchShopInventorySerializer_iDukaan(inv, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)
    

    def destroy(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == emp_manager:
            try:
                ShopModel.ShopInventory.objects.get(id=request.data['id']).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ShopModel.ShopInventory.DoesNotExist:
                return error_response(shop_inv_not_found)
        
        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)


class ShopGstPostGetAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == 1:
            serializer = ShopSerializer.AddIrShopGstSerializer_iDukaan(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)

    def list(self, request, *args, **kwargs):
        check = validate_org_shop_emp(request.user, kwargs['shopid'], kwargs['orgid'])
        if check == 1:
            gst = ShopModel.ShopGst.objects.filter(org=kwargs['orgid'], shop=kwargs['shopid'])
            if gst.count() > 0:
                serializer = ShopSerializer.ShopGstSerializer_iDukaan(gst, many=True)
                response_map['data'] = serializer.data
                return Response(response_map, status=status.HTTP_200_OK)
            return error_response(shop_gst_not_found)

        elif check == emp_non_manager:
            return error_response(organization_shop_employee_failed_manager)

        return error_response(is_error)
