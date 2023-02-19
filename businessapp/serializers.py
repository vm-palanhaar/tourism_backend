from rest_framework import serializers

from businessapp import models as BusinessModel
from userapp import models as UserModel


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
        model = BusinessModel.OrganizationType
        fields = '__all__'


class AddOrganizationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = BusinessModel.Organization
        exclude = ['active']

    def create(self, validated_data):
        try:
            org = BusinessModel.Organization.objects.get(registration=validated_data['registration'])
            return org
        except BusinessModel.Organization.DoesNotExist:
            org = super().create(validated_data)
            user = self.context.get('view').request.user
            employee = BusinessModel.OrganizationEmployee.objects.create(
                organization = org,
                user = user,
                manager = True
            )
            employee.save
            return org


class OrganizationListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    entity = serializers.CharField()
    class Meta:
        model = BusinessModel.Organization
        exclude = ['registration','document','created_at','updated_at']


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    entity = serializers.CharField()
    employees = serializers.SerializerMethodField()
    class Meta:
        model = BusinessModel.Organization
        fields = ['id','entity','name','employees']
    
    def get_employees(self, instance):
        return BusinessModel.OrganizationEmployee.objects.filter(organization=instance).count()
    

class AddOrganizationEmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = BusinessModel.OrganizationEmployee
        fields = '__all__'


class UpdateOrganizationEmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = BusinessModel.OrganizationEmployee
        fields = ['id','manager']


class OrganizationEmployeeListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    class Meta:
        model = BusinessModel.OrganizationEmployee
        exclude = ['user']

    def get_name(self, instance):
        user = UserModel.User.objects.get(username=instance.user)
        return f'{user.first_name} {user.last_name}'

    def get_organization(self, instance):
        return f'{instance.organization.id}'
    