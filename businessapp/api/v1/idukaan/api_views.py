from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from userapp import permissions as UserPerm
from businessapp import models as OrgModel
from userapp import models as UserModel
from businessapp import serializers as OrgSerializer

from businessapp.api import errors as OrgError
from userapp.api import errors as UserError

'''
PROD
1. OrgTypesApi
2. OrgApi
3. OrgEmpApi
4. OrgStateGstApi
DEV
'''


'''
1 : Manager
0 : Employee
-1 : Does not exist -> user account de-activation
'''
def validate_org_emp(user, org):
    try:
        emp = OrgModel.OrgEmp.objects.get(user=user, org=org)
        if emp.is_manager == True:
            return 1
        return 0
    except OrgModel.OrgEmp.DoesNotExist:
        return -1
    
def validate_emp(user, org):
        try:
            return OrgModel.OrgEmp.objects.get(user=user, org=org)
        except OrgModel.OrgEmp.DoesNotExist:
            return None
        
def error_response_400(response_fail):
    return Response(response_fail, status=status.HTTP_400_BAD_REQUEST)

def error_response_401(response_fail):
    return Response(response_fail, status=status.HTTP_401_UNAUTHORIZED)

def error_response_409(response_fail):
    return Response(response_fail, status=status.HTTP_409_CONFLICT)


class OrgTypesApi(generics.ListAPIView, PermissionRequiredMixin):
    queryset = OrgModel.OrgType.objects.all()
    serializer_class = OrgSerializer.OrgTypesSerializer
    permission_classes = [IsAuthenticated]


class OrgApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        serializer = OrgSerializer.AddOrgSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            response_data['org'] = serializer.data
            response_data['message'] = 'Thanks for registering your organization with us.'
            return Response(response_data, status=status.HTTP_201_CREATED)
        if 'reg_no' in serializer.data:
            response_data['error'] = OrgError.error_business_org_found
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
    def list(self, request, *args, **kwargs):
        response_data = {}
        queryset = request.user.orgemp_set.all()
        if queryset.count() > 0:
            orgs = []
            for org in queryset:
                orgs.append(OrgSerializer.OrgListSerializer(org.org).data)
            response_data['orgList'] = orgs
            return Response(response_data, status=status.HTTP_200_OK)
        response_data['error'] = OrgError.error_business_org_emp_not_found_request_user
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        response_data = {}
        org_emp = validate_org_emp(request.user, kwargs['orgId'])
        if org_emp == 1 or org_emp == 0:
            org = OrgModel.Org.objects.get(id = kwargs['orgId'])
            serializer = OrgSerializer.OrgInfoSerializer(org)
            return Response(serializer.data, status=status.HTTP_200_OK)
        response_data['error'] = OrgError.error_business_org_emp_not_found_request_user
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class OrgEmpApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        # Validate OrgId from headers and url arguments
        if kwargs['orgId'] == request.data['org']:
            org_emp = validate_emp(request.user, kwargs['orgId'])
            if org_emp.is_manager == True:
                try:
                    emp = OrgModel.OrgEmp.objects.get(user = request.data['user'], org = request.data['org'])
                    OrgError.error_org_add_emp_found['message'] = f'{emp.user.first_name} {emp.user.last_name} is already associated with {emp.org.name}'
                    response_data['error'] = OrgError.error_org_add_emp_found
                    return Response(response_data, status=status.HTTP_409_CONFLICT)
                except OrgModel.OrgEmp.DoesNotExist:
                    try:
                        user = UserModel.User.objects.get(username = request.data['user'])
                    except UserModel.User.DoesNotExist:
                        response_data['error'] = UserError.error_user_invalid
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    if user.is_active == False and user.is_verified == False:
                        UserError.error_user_inactive_notverified['message'] = f'{user.first_name} {user.last_name}\'s account is not active and verified!'
                        response_data['error'] = UserError.error_user_inactive_notverified
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    elif user.is_active == False:
                        UserError.error_user_inactive['message'] = f'{user.first_name} {user.last_name}\'s account is not active!'
                        response_data['error'] = UserError.error_user_inactive
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    elif user.is_verified ==  False:
                        UserError.error_user_notverified['message'] = f'{user.first_name} {user.last_name}\'s account is not verified!'
                        response_data['error'] = UserError.error_user_notverified
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    # PROD - To prevent Palanhaar employees mail compromise
                    elif user.is_staff or user.is_superuser or '@palanhaar.in' in request.data['user']:
                        request.user.is_active = False
                        request.user.save()
                        response_data['error'] = OrgError.error_bad_action
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    serializer = OrgSerializer.AddOrgEmpSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['orgEmp'] = serializer.data
                        response_data['message'] = f'{user.first_name} {user.last_name} is associated with {org_emp.org.name}'
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif org_emp.is_manager == False:
                response_data['error'] = OrgError.error_business_org_emp_not_mng
                return error_response_400(response_data) 
            response_data['error'] = OrgError.error_business_org_emp_not_found_request_user
            return error_response_400(response_data)
        request.user.is_active = False
        request.user.save()
        response_data['error'] = OrgError.error_bad_action
        return error_response_400(response_data)

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        org_emp = validate_org_emp(request.user, kwargs['orgId'])
        if org_emp == 1 or org_emp == 0:
            employees = OrgModel.OrgEmp.objects.filter(org=kwargs['orgId'])
            serializer = OrgSerializer.OrgEmpListSerializer(employees, many=True)
            response_data['orgEmpList'] = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        
        response_data['error'] = OrgError.error_business_org_emp_not_found_request_user
        return error_response_400(response_data)
    
    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = str(request.data['id'])
        response_data['orgId'] = kwargs['orgId']
        # Validate OrgId from headers and url arguments
        if kwargs['orgEmpId'] == str(request.data['id']):
            org_emp = validate_org_emp(request.user, kwargs['orgId'])
            if org_emp == 1:
                try:
                    emp = OrgModel.OrgEmp.objects.get(id = request.data['id'])
                except OrgModel.OrgEmp.DoesNotExist:
                    response_data['error'] = OrgError.error_business_org_emp_not_found
                    return error_response_400(response_data)
                if request.user == emp.user:
                    response_data['error'] = OrgError.error_business_org_emp_self_update_delete
                    return error_response_400(response_data)
                serializer = OrgSerializer.UpdateOrgEmpSerializer(emp, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(response_data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif org_emp == 0:
                response_data['error'] = OrgError.error_business_org_emp_not_mng
                return error_response_400(response_data)
            response_data['error'] = OrgError.error_business_org_emp_not_found_request_user
            return error_response_400(response_data)
        request.user.is_active = False
        request.user.save()
        response_data['error'] = OrgError.error_bad_action
        return error_response_400(response_data)

    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        response_data['id'] = str(request.data['id'])
        # Validate OrgId from headers and url arguments
        if kwargs['orgEmpId'] == str(request.data['id']):
            org_emp = validate_org_emp(request.user, kwargs['orgId'])
            if org_emp == 1:
                try:
                    emp = OrgModel.OrgEmp.objects.get(id = request.data['id'])
                except OrgModel.OrgEmp.DoesNotExist:
                    response_data['error'] = OrgError.error_business_org_emp_not_found
                    return error_response_400(response_data)
                if request.user == emp.user:
                    response_data['error'] = OrgError.error_business_org_emp_self_update_delete
                    return error_response_400(response_data)
                emp.delete()
                return Response(response_data, status=status.HTTP_200_OK)
            elif org_emp == 0:
                response_data['error'] = OrgError.error_business_org_emp_not_mng
                return error_response_400(response_data)
            response_data['error'] = OrgError.error_business_org_emp_not_found_request_user
            return error_response_400(response_data)
        request.user.is_active = False
        request.user.save()
        response_data['error'] = OrgError.error_bad_action
        return error_response_400(response_data)


class OrgStateGstApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        # Validate OrgId from headers and url arguments
        if kwargs['orgId'] == request.data['org']:
            org_emp = validate_org_emp(request.user, kwargs['orgId'])
            if org_emp == 1:
                try:
                    OrgModel.OrgStateGstOps.objects.get(gstin = request.data['gstin'])
                    response_data['error'] = OrgError.error_business_org_ops_found
                    return error_response_409(response_data)
                except OrgModel.OrgStateGstOps.DoesNotExist:
                    pass
                serializer = OrgSerializer.AddOrgStateGstOpsSerializer(data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['orgOps'] = serializer.data
                    return Response(response_data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif org_emp == 0:
                response_data['error'] = OrgError.error_business_org_emp_not_mng
                return error_response_400(response_data)
            response_data['error'] = OrgError.error_business_org_emp_not_found_request_user
            return error_response_400(response_data)
        request.user.is_active = False
        request.user.save()
        response_data['error'] = OrgError.error_bad_action
        return error_response_400(response_data)

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        org_emp = validate_org_emp(request.user, kwargs['orgId'])
        if org_emp == 1:
            ops = OrgModel.OrgStateGstOps.objects.filter(org = kwargs['orgId'])
            if ops.count() > 0:
                serializer = OrgSerializer.OrgStateGstOpsListSerializer(ops, many=True)
                response_data['opsList'] = serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            response_data['error'] = OrgError.error_business_org_ops_not_found
            return error_response_400(response_data)
        elif org_emp == 0:
            response_data['error'] = OrgError.error_business_org_emp_not_mng
            return error_response_400(response_data)
        response_data['error'] = OrgError.error_business_org_emp_not_found_request_user
        return error_response_400(response_data)

