from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from userapp import permissions as UserPerm
from businessapp import models as OrgModel
from userapp import models as UserModel
from businessapp import serializers as OrgSerializer

from businessapp.api import errors as OrgError
from userapp.api import errors as UserError
from apiutil import errors as UtilError

'''
PROD
1. OrgTypesApi
2. OrgApi
3. OrgEmpApi
4. OrgStateGstApi
DEV
'''
    
def validateOrgEmpObj(user, org):
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
            return error_response_409(OrgError.businessOrgFound())
        return error_response_400(UtilError.bodyEmptyFields())
            
    def list(self, request, *args, **kwargs):
        response_data = {}
        queryset = request.user.orgemp_set.all()
        if queryset.count() > 0:
            orgs = []
            for org in queryset:
                orgs.append(OrgSerializer.OrgListSerializer(org.org).data)
            response_data['orgList'] = orgs
            return Response(response_data, status=status.HTTP_200_OK)
        return error_response_400(OrgError.businessOrgListNotFound())
    
    def retrieve(self, request, *args, **kwargs):
        org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
        if org_emp != None:
            org = OrgModel.Org.objects.get(id = kwargs['orgId'])
            serializer = OrgSerializer.OrgInfoSerializer(org)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return error_response_400(OrgError.businessOrgEmpSelfNotFound())


class OrgEmpApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        # Validate OrgId from headers and url arguments
        if kwargs['orgId'] == request.data['org']:
            org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
            if org_emp != None and org_emp.org.is_active == True and org_emp.is_manager == True:
                try:
                    emp = OrgModel.OrgEmp.objects.get(user = request.data['user'], org = request.data['org'])
                    response_data.update(OrgError.businessOrgEmpFound(emp))
                    return error_response_409(response_data)
                except OrgModel.OrgEmp.DoesNotExist:
                    try:
                        user = UserModel.User.objects.get(username = request.data['user'])
                    except UserModel.User.DoesNotExist:
                        response_data.update(UserError.userInvalid())
                        return error_response_400(response_data)
                    if user.is_active == False and user.is_verified == False:
                        response_data.update(UserError.userInActiveNotVerified())
                        return error_response_400(response_data)
                    elif user.is_active == False:
                        response_data.update(UserError.userInActive())
                        return error_response_400(response_data)
                    elif user.is_verified ==  False:
                        response_data.update(UserError.userNotVerified())
                        return error_response_400(response_data)
                    # PROD - To prevent Palanhaar employees mail compromise
                    elif user.is_staff or user.is_superuser or '@palanhaar.in' in request.data['user']:
                        request.user.is_active = False
                        request.user.save()
                        response_data.update(UtilError.badActionUser(request, 'Adding Palanhaar Employees'))
                        return error_response_400(response_data)
                    serializer = OrgSerializer.AddOrgEmpSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['orgEmp'] = serializer.data
                        response_data['message'] = f'{user.first_name} {user.last_name} is associated with {org_emp.org.name}'
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    response_data.update(UtilError.bodyEmptyFields())
                    return error_response_400(response_data)
            elif org_emp != None and org_emp.org.is_active == True and org_emp.is_manager == False:
                response_data.update(OrgError.businessOrgEmpNotMng(org_emp.org.name))
                return error_response_400(response_data)
            elif org_emp != None and org_emp.org.is_active == False:
                response_data.update(OrgError.businessOrgNotVerified(org_emp.org.name))
                return error_response_400(response_data)
            response_data.update(OrgError.businessOrgEmpSelfNotFound())
            return error_response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'OrgEmpApiCreate_OrgId_Url-{0}_HB-{1}'.format(kwargs['orgId'], request.data['org'])))
        return error_response_401(response_data)

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
        if org_emp != None:
            employees = OrgModel.OrgEmp.objects.filter(org=kwargs['orgId'])
            serializer = OrgSerializer.OrgEmpListSerializer(employees, many=True)
            response_data['orgName'] = org_emp.org.name
            response_data['orgEmpList'] = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        response_data.update(OrgError.businessOrgEmpSelfNotFound())
        return error_response_400(response_data)
    
    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = str(request.data['id'])
        response_data['orgId'] = kwargs['orgId']
        # Validate OrgEmpId from body and url arguments
        if kwargs['orgEmpId'] == str(request.data['id']):
            org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
            if org_emp != None and org_emp.org.is_active == True and org_emp.is_manager == True:
                try:
                    emp = OrgModel.OrgEmp.objects.get(id = request.data['id'])
                except OrgModel.OrgEmp.DoesNotExist:
                    response_data.update(OrgError.businessOrgEmpNotFound(org_emp.org.name))
                    return error_response_400(response_data)
                if request.user == emp.user:
                    response_data.update(OrgError.businessOrgEmpSelfUd(emp.org.name))
                    return error_response_400(response_data)
                serializer = OrgSerializer.UpdateOrgEmpSerializer(emp, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(response_data, status=status.HTTP_200_OK)
                response_data.update(UtilError.bodyEmptyFields())
                return error_response_400(response_data)
            elif org_emp != None and org_emp.org.is_active == True and org_emp.is_manager == False:
                response_data.update(OrgError.businessOrgEmpNotMng(org_emp.org.name))
                return error_response_400(response_data)
            elif org_emp != None and org_emp.org.is_active == False:
                response_data.update(OrgError.businessOrgNotVerified(org_emp.org.name))
                return error_response_400(response_data)
            response_data.update(OrgError.businessOrgEmpSelfNotFound())
            return error_response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'OrgEmpApiPatch_OrgEmpId_Url-{0}_HB-{1}'.format(kwargs['orgEmpId'], request.data['id'])))
        return error_response_401(response_data)

    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        response_data['id'] = str(request.data['id'])
        # Validate OrgEmpId from body and url arguments
        if kwargs['orgEmpId'] == str(request.data['id']):
            org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
            if org_emp != None and org_emp.org.is_active == True and org_emp.is_manager == True:
                try:
                    emp = OrgModel.OrgEmp.objects.get(id = request.data['id'])
                except OrgModel.OrgEmp.DoesNotExist:
                    response_data.update(OrgError.businessOrgEmpNotFound(org_emp.org.name))
                    return error_response_400(response_data)
                if request.user == emp.user:
                    response_data.update(OrgError.businessOrgEmpSelfUd(emp.org.name))
                    return error_response_400(response_data)
                emp.delete()
                return Response(response_data, status=status.HTTP_200_OK)
            elif org_emp != None and org_emp.org.is_active == True and org_emp.is_manager == False:
                response_data.update(OrgError.businessOrgEmpNotMng(org_emp.org.name))
                return error_response_400(response_data)
            elif org_emp != None and org_emp.org.is_active == False:
                response_data.update(OrgError.businessOrgNotVerified(org_emp.org.name))
            response_data.update(OrgError.businessOrgEmpSelfNotFound())
            return error_response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'OrgEmpApiDelete_OrgEmpId_Url-{0}_HB-{1}'.format(kwargs['orgEmpId'], request.data['id'])))
        return error_response_401(response_data)


class OrgStateGstApi(viewsets.ViewSet, PermissionRequiredMixin):
    permission_classes = [IsAuthenticated,UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        # Validate OrgId from body and url arguments
        if kwargs['orgId'] == request.data['org']:
            org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
            if org_emp != None and org_emp.org.is_active == True and org_emp.is_manager == True:
                try:
                    OrgModel.OrgStateGstOps.objects.get(gstin = request.data['gstin'])
                    response_data.update(OrgError.businessOrgOpsFound())
                    return error_response_409(response_data)
                except OrgModel.OrgStateGstOps.DoesNotExist:
                    serializer = OrgSerializer.AddOrgStateGstOpsSerializer(data = request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['orgOps'] = serializer.data
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    response_data.update(UtilError.bodyEmptyFields())
                    return error_response_400(response_data)
            elif org_emp != None and org_emp.org.is_active == True and org_emp.is_manager == False:       
                response_data.update(OrgError.businessOrgEmpNotMng(org_emp.org.name))
                return error_response_400(response_data)
            elif org_emp != None and org_emp.org.is_active == False:
                response_data.update(OrgError.businessOrgNotVerified(org_emp.org.name))
                return error_response_400(response_data)
            response_data.update(OrgError.businessOrgEmpSelfNotFound())
            return error_response_400(response_data)
        response_data.update(UtilError.badActionUser(request, 'OrgStateGstApiCreate_OrgId_Url-{0}_HB-{1}'.format(kwargs['orgId'], request.data['org'])))
        return error_response_401(response_data)

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
        if org_emp != None:
            response_data['orgName'] = org_emp.org.name
            if org_emp.is_manager == True:
                ops = OrgModel.OrgStateGstOps.objects.filter(org = kwargs['orgId'])
                if ops.count() > 0:
                    serializer = OrgSerializer.OrgStateGstOpsListSerializer(ops, many=True)
                    response_data['opsList'] = serializer.data
                    return Response(response_data, status=status.HTTP_200_OK)
                response_data.update(OrgError.businessOrgOpsNotFound(org_emp.org.name))
                return error_response_400(response_data)
            elif org_emp.is_manager == False:
                response_data.update(OrgError.businessOrgEmpNotMng(org_emp.org.name))
                return error_response_400(response_data)
        response_data.update(OrgError.businessOrgEmpSelfNotFound())
        return error_response_400(response_data)
