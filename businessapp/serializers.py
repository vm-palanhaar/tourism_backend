from rest_framework import serializers

from businessapp import models as OrgModel
from userapp import models as UserModel
from indianrailwaysapp import models as IRModel
from indianrailwaysapp import serializers as IRSerializer


'''
iDukaan APIs Serializer
1. OrgTypesSerializer
2. AddOrgSerializer
3. OrgListSerializer
4. OrgInfoSerializer
5. AddOrgEmpSerializer
6. UpdateOrgEmpSerializer
7. OrgEmpListSerializer
8. AddOrgStateGstOpsSerializer
9. OrgStateGstOpsListSerializer
'''

class OrgTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgModel.OrgType
        fields = '__all__'


class AddOrgSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    doc = serializers.FileField(write_only=True)
    class Meta:
        model = OrgModel.Org
        exclude = ['is_active','created_at','updated_at']

    def create(self, validated_data):
        org = super().create(validated_data)
        org_emp = OrgModel.OrgEmp.objects.create(
            org = org,
            user = self.context.get('user'),
            is_manager = True
        )
        org_emp.save
        return org


class OrgListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    type = serializers.CharField()
    irShops = serializers.SerializerMethodField()
    class Meta:
        model = OrgModel.Org
        exclude = ['reg_no','doc','created_at','updated_at']

    def get_irShops(self, instance):
        shops = IRModel.OrganizationShop.objects.filter(organization=instance).count()
        return shops


class OrgInfoSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    type = serializers.CharField()
    emp = serializers.SerializerMethodField()
    irShops = serializers.SerializerMethodField()
    class Meta:
        model = OrgModel.Org
        fields = ['id','name','type','emp','irShops']
    
    def get_emp(self, instance):
        return OrgModel.OrgEmp.objects.filter(org=instance).count()
    
    def get_irShops(self, instance):
        shops = IRModel.OrganizationShop.objects.filter(organization=instance).count()
        return shops
    

class AddOrgEmpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = OrgModel.OrgEmp
        exclude = ['created_at','updated_at']


class UpdateOrgEmpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = OrgModel.OrgEmp
        fields = ['id','is_manager']


class OrgEmpListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = OrgModel.OrgEmp
        exclude = ['user','org','created_at','updated_at']

    def get_name(self, instance):
        user = UserModel.User.objects.get(username=instance.user)
        return f'{user.first_name} {user.last_name}'



class AddOrgStateGstOpsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False, read_only=True)
    gstin = serializers.CharField(required=True)
    doc = serializers.FileField(write_only=True)
    class Meta:
        model = OrgModel.OrgStateGstOps
        exclude = ['created_at','updated_at','is_active']


class OrgStateGstOpsListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    state = serializers.CharField()
    class Meta:
        model = OrgModel.OrgStateGstOps
        exclude = ['doc','created_at','updated_at','org']