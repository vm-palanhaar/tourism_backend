from rest_framework import serializers

from businessapp import models as OrgModel
from userapp import models as UserModel
from indianrailwaysapp import models as IRModel
from indianrailwaysapp import serializers as IRSerializer


'''
iDukaan APIs Serializer
1. OrganizationTypeListSerializer
2. AddOrganizationSerializer
3. OrganizationListSerializer
4. OrganizationSerializer
5. AddOrganizationEmployeeSerializer
6. UpdateOrganizationEmployeeSerializer
7. OrganizationEmployeeListSerializer
'''

class OrganizationTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgModel.OrganizationType
        fields = '__all__'


class AddOrganizationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = OrgModel.Organization
        exclude = ['is_active']

    def create(self, validated_data):
        org = super().create(validated_data)
        user = self.context.get('view').request.user
        employee = OrgModel.OrganizationEmployee.objects.create(
            organization = org,
            user = user,
            manager = True
        )
        employee.save
        return org


class OrganizationListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    entity = serializers.CharField()
    ir_shops = serializers.SerializerMethodField()
    class Meta:
        model = OrgModel.Organization
        exclude = ['registration','document','created_at','updated_at']

    def get_ir_shops(self, instance):
        shops = IRModel.OrganizationShop.objects.filter(organization=instance).count()
        return shops


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    entity = serializers.CharField()
    employees = serializers.SerializerMethodField()
    ir_shops = serializers.SerializerMethodField()
    class Meta:
        model = OrgModel.Organization
        fields = ['id','entity','name','employees','ir_shops']
    
    def get_employees(self, instance):
        return OrgModel.OrganizationEmployee.objects.filter(organization=instance).count()
    
    def get_ir_shops(self, instance):
        shops = IRModel.OrganizationShop.objects.filter(organization=instance).count()
        return shops
    

class AddOrganizationEmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = OrgModel.OrganizationEmployee
        fields = '__all__'


class UpdateOrganizationEmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = OrgModel.OrganizationEmployee
        fields = ['id','manager']


class OrganizationEmployeeListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    class Meta:
        model = OrgModel.OrganizationEmployee
        exclude = ['user']

    def get_name(self, instance):
        user = UserModel.User.objects.get(username=instance.user)
        return f'{user.first_name} {user.last_name}'

    def get_organization(self, instance):
        return f'{instance.organization.id}'
    