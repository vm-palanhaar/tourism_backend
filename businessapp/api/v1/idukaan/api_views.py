from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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

is_error = 'Something went wrong. Issue reported to Team and your account will be de-activated.'

organization_add_failed_already_exist = 'Organization already exists!'
organization_employee_not_found = 'You are not assiociated with the organization!'
organization_add_employee_already_exist = 'User is already associated with organization!'
organization_update_delete_employee_not_found = 'User is not associated with organization!'
user_not_found = 'User does not exist!'
organization_employee_failed_manager = 'You are not authorized to update organization!'
organization_update_delete_self_employee = 'Bad action!'
org_state_gst_not_found = 'Organization do not support inter-state operations'

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
        
def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


class OrganizationTypeListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    queryset = OrgModel.OrganizationType.objects.all()
    serializer_class = OrgSerializer.OrganizationTypeListSerializer
    permission_classes = [IsAuthenticated]


class AddOrganizationAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    queryset = OrgModel.Organization.objects.all()
    serializer_class = OrgSerializer.AddOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            OrgModel.Organization.objects.get(registration=request.data['registration'])
            return error_response(organization_add_failed_already_exist)
        except OrgModel.Organization.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_map['data'] = serializer.data
                return Response(response_map, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = OrgSerializer.OrganizationListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = request.user.organizationemployee_set.all()
        if queryset.count() > 0:
            organizations = []
            for organization in queryset:
                organizations.append(self.get_serializer(organization.organization).data)
            response_map['data'] = organizations
            return Response(response_map, status=status.HTTP_200_OK)
        
        return error_response(organization_employee_not_found)


class OrganizationDetailsAPIView(generics.RetrieveAPIView, PermissionRequiredMixin):
    serializer_class = OrgSerializer.OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, kwargs['orgid'])
        if check:
            organization = OrgModel.Organization.objects.get(id=kwargs['orgid'])
            serializer =self.get_serializer(organization)
            response_map['data'] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)
        
        return error_response(is_error)


class AddOrganizationEmployeeAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    serializer_class = OrgSerializer.AddOrganizationEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, request.data['organization'])
        if check == 1:
            try:
                OrgModel.OrganizationEmployee.objects.get(user=request.data['user'], 
                                                        organization=request.data['organization'])
                return error_response(organization_add_employee_already_exist)
            except OrgModel.OrganizationEmployee.DoesNotExist:
                try:
                    UserModel.User.objects.get(username=request.data['user'])
                except UserModel.User.DoesNotExist:
                    return error_response(user_not_found)
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif check == 0:
            return error_response(organization_employee_failed_manager)
        
        return error_response(is_error)


class OrganizationEmployeeListAPIView(generics.ListAPIView, PermissionRequiredMixin):
    serializer_class = OrgSerializer.OrganizationEmployeeListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, kwargs['orgid'])
        if check == 1 or check == 0:
            employees = OrgModel.OrganizationEmployee.objects.filter(organization=kwargs['orgid'])
            serializer = self.get_serializer(employees, many=True)
            response_map['data'] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)
        
        return error_response(is_error)


class OrganizationEmployeeAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, kwargs['orgid'])
        if check == 1:
            emp = validate_emp(request.data['id'], kwargs['orgid'])
            if emp != None:
                if request.user == emp.user:
                    return error_response(organization_update_delete_self_employee)
                serializer = OrgSerializer.OrganizationEmployeeListSerializer(emp, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return error_response(organization_update_delete_employee_not_found)

        elif check == 0:
            return error_response(organization_employee_failed_manager)
        
        return error_response(is_error)


    def destroy(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, kwargs['orgid'])
        if check == 1:
            emp = validate_emp(kwargs['empid'], kwargs['orgid'])
            if emp != None:
                if request.user == emp.user:
                    return error_response(organization_update_delete_self_employee)
                emp.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return error_response(organization_update_delete_employee_not_found)

        elif check == 0:
            return error_response(organization_employee_failed_manager)
        
        return error_response(is_error)


class OrgStateGstAPIViewset(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, kwargs['orgid'])
        if check == 1:
            serializer = OrgSerializer.AddOrgStateGstOpsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif check == 0:
            return error_response(organization_employee_failed_manager)
        
        return error_response(is_error)


    def list(self, request, *args, **kwargs):
        check = validate_org_emp(request.user, kwargs['orgid'])
        if check == 1:
            ops = OrgModel.OrgStateGstOps.objects.filter(org = kwargs['orgid'])
            if ops.count() > 0:
                serializer = OrgSerializer.OrgStateGstOpsListSerializer(ops, many=True)
                response_map['data'] = serializer.data
                return Response(response_map, status=status.HTTP_200_OK)
            return error_response(org_state_gst_not_found)

        elif check == 0:
            return error_response(organization_employee_failed_manager)
        
        return error_response(is_error)
