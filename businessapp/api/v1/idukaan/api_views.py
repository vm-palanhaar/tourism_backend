from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from userapp import permissions as UserPerm
from businessapp import models as OrgModel
from userapp import models as UserModel
from businessapp import serializers as OrgSerializer

'''
PROD
1. OrganizationTypeListApi
2. AddOrganizationApi
3. OrganizationListApi
4. OrganizationDetailsApi
5. AddOrganizationEmployeeApi
6. OrganizationEmployeeListApi
7. DeleteOrganizationEmployeeApi
DEV
'''

failed_response_map = {'error':None}
response_map = {'data':None}

error_bad_action = 'Bad Action! Issue reported to Team and account will be de-activated!'

error_org_exists = 'org_exists'
error_org_emp_not_found = 'You are not association with the organization!'
error_org_add_emp_already_exist = 'User is already associated with organization!'
error_org_update_delete_emp_not_found = 'User is not associated with organization!'
error_user_not_found = 'User does not exist!'
error_org_emp_failed_manager = 'You are not authorized to view/update resource in organization!'
error_org_update_delete_self_emp = 'Bad action!'
error_org_state_gst_not_found = 'Organization do not support inter-state operations'

'''
1 : Manager
0 : Employee
-1 : Does not exist -> user account de-activation
'''
def validate_org_emp(user, org):
    try:
        emp = OrgModel.OrganizationEmployee.objects.get(user=user, organization=org)
        if emp.manager == True:
            return 1
        return 0
    except OrgModel.OrganizationEmployee.DoesNotExist:
        return -1
    
def validate_emp(user, org):
        try:
            return OrgModel.OrganizationEmployee.objects.get(id=user, organization=org)
        except OrgModel.OrganizationEmployee.DoesNotExist:
            return None
        
def error_response_400(response_fail):
    return Response(response_fail, status=status.HTTP_400_BAD_REQUEST)

def error_response_401(response_fail):
    return Response(response_fail, status=status.HTTP_401_UNAUTHORIZED)


class OrgTypesApi(generics.ListAPIView, PermissionRequiredMixin):
    queryset = OrgModel.OrganizationType.objects.all()
    serializer_class = OrgSerializer.OrgTypesSerializer
    permission_classes = [IsAuthenticated]


class OrgApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        try:
            org = OrgModel.Organization.objects.get(registration=request.data['registration'])
            response_data['id'] = org.id
            response_data['error'] = {
                'code' : error_org_exists,
                'message' : 'The registration number you entered already exists in our iDukaan app. Please double-check the registration number and try again. If you need further information or assistance, we recommend raising a request for more information.'
            }
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        except OrgModel.Organization.DoesNotExist:
            serializer = OrgSerializer.AddOrgSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'id' : serializer.data['id'],
                    'msg' : 'Hello'
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        response_data = {}
        # Org Info
        if 'id' in request.headers:
            check = validate_org_emp(request.user, request.headers['id'])
            if check == 0 or check == 1:
                org = OrgModel.Organization.objects.get(id=request.headers['id'])
                serializer =OrgSerializer.OrgInfoSerializer(org)
                response_data = serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            response_data['msg'] = error_bad_action
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        # Org List
        queryset = request.user.organizationemployee_set.all()
        if queryset.count() > 0:
            orgs = []
            for org in queryset:
                orgs.append(OrgSerializer.OrgListSerializer(org.organization).data)
            response_data['org'] = orgs
            return Response(response_data, status=status.HTTP_200_OK)
        response_data['msg'] = error_org_emp_not_found
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class OrgEmpApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        # To validate Headers and Url argument
        if kwargs['orgId'] == request.data['organization']:
            emp_manager = validate_org_emp(request.user, request.data['organization'])
            if emp_manager == 1:
                try:
                    orgEmp = OrgModel.OrganizationEmployee.objects.get(user=request.data['user'], organization=request.data['organization'])
                    response_data['msg'] = f'{orgEmp.user.first_name} {orgEmp.user.last_name} is already associated with {orgEmp.organization.name}'
                    return Response(response_data, status=status.HTTP_409_CONFLICT)
                except OrgModel.OrganizationEmployee.DoesNotExist:
                    try:
                        user = UserModel.User.objects.get(username=request.data['user'], is_verified=True)
                    except UserModel.User.DoesNotExist:
                        response_data['msg'] = error_user_not_found
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    serializer = OrgSerializer.AddOrgEmpSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['msg'] = f'{user.first_name} {user.last_name}'
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            elif emp_manager == 0:
                response_data['error'] = error_org_emp_failed_manager
                return error_response_400(response_data)
            
        response_data['error'] = error_bad_action
        return error_response_400(response_data)
    

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        check = validate_org_emp(request.user, kwargs['orgId'])
        if check == 1 or check == 0:
            employees = OrgModel.OrganizationEmployee.objects.filter(organization=kwargs['orgId'])
            serializer = OrgSerializer.OrgEmpListSerializer(employees, many=True)
            response_data['orgEmpList'] = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        
        response_data['error'] = error_bad_action
        return error_response_400(response_data)
    

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = str(request.data['id'])
        response_data['orgId'] = kwargs['orgId']
        check = validate_org_emp(request.user, kwargs['orgId'])
        if check == 1:
            emp = validate_emp(request.data['id'], kwargs['orgId'])
            if emp != None:
                if request.user == emp.user:
                    response_data['error'] = error_org_update_delete_self_emp
                    return error_response_400(response_data)
                serializer = OrgSerializer.UpdateOrgEmpSerializer(emp, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(response_data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            response_data['error'] = error_org_update_delete_emp_not_found
            return error_response_400(response_data)

        elif check == 0:
            response_data['error'] = error_org_emp_failed_manager
            return error_response_400(response_data)
        
        response_data['error'] = error_bad_action
        return error_response_400(response_data)


    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        response_data['orgEmpId'] = str(request.data['id'])
        check = validate_org_emp(request.user, kwargs['orgId'])
        if check == 1:
            emp = validate_emp(request.data['id'], kwargs['orgId'])
            if emp != None:
                if request.user == emp.user:
                    response_data['error'] = error_org_update_delete_self_emp
                    return error_response_400(response_data)
                emp.delete()
                return Response(response_data, status=status.HTTP_204_NO_CONTENT)
            
            response_data['error'] = error_org_update_delete_emp_not_found
            return error_response_400(response_data)

        elif check == 0:
            response_data['error'] = error_org_emp_failed_manager
            return error_response_400(response_data)
        
        response_data['error'] = error_bad_action
        return error_response_400(response_data)


class OrgStateGstAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        check = validate_org_emp(request.user, kwargs['orgId'])
        if check == 1:
            serializer = OrgSerializer.AddOrgStateGstOpsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif check == 0:
            response_data['error'] = error_org_emp_failed_manager
            return error_response_400(response_data)
        
        response_data['error'] = error_bad_action
        return error_response_400(response_data)


    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        check = validate_org_emp(request.user, kwargs['orgId'])
        if check == 1:
            ops = OrgModel.OrgStateGstOps.objects.filter(org = kwargs['orgId'])
            if ops.count() > 0:
                serializer = OrgSerializer.OrgStateGstOpsListSerializer(ops, many=True)
                response_data['opsList'] = serializer.data
                return Response(response_map, status=status.HTTP_200_OK)
            
            response_data['error'] = error_org_state_gst_not_found
            return error_response_400(response_data)

        elif check == 0:
            response_data['error'] = error_org_emp_failed_manager
            return error_response_400(response_data)
        
        response_data['error'] = error_bad_action
        return error_response_400(response_data)
