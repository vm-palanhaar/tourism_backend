from rest_framework import serializers

from indianrailwaysapp import models
from userapp import models as UserModel
from productapp import serializers as PcSerializer
from businessapp import models as OrgModel

'''
Common APIs Serializer
1. RailwayStationListSerializer
2. ShopInventoryListSerializer

Yatrigan APIs Serializer
1. ShopListSerializer_Yatrigan
2. ShopDetailsSerializer_Yatrigan

iDukaan APIs Serializer
1. AddShopSerializer_iDukaan
2. ShopListSerializer_iDukaan
3. OrganizationShopListSerializer_iDukaan
4. PatchShopSerializer_iDukaan
5. ShopDetailsSerializer_iDukaan
6. AddOrgShopEmpSerializer_iDukaan
7. OrgShopEmpListSerializer_iDukaan
8. UpdateOrgShopEmpSerializer_iDukaan

'''

#Common
class RailwayStationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RailwayStation
        fields = ['code','name']


#Common
class ShopInventoryListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    shop = serializers.SerializerMethodField()
    product= serializers.SerializerMethodField()
    class Meta:
        model = models.ShopInventory
        exclude = ['created_at','updated_at']

    def get_shop(self, instance):
        return f'{instance.shop.id}'

    def get_product(self, instance):
        return PcSerializer.ProductSerializer(instance.product).data


#Yatrigan
class ShopListSerializer_Yatrigan(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = ['name','image','station','platform_a','platform_b']


#Yatrigan
class ShopDetailsSerializer_Yatrigan(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = ['id','name','image','contact_number',
                    'station','platform_a','platform_b',
                    'is_cash','is_card','is_upi']


#iDukaan
class AddShopSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    organization = serializers.CharField(required=True)
    lic_number = serializers.CharField(required=True)
    lic_cert = serializers.FileField(required=False)
    lic_start_date = serializers.DateField(required=True)
    lic_end_date = serializers.DateField(required=True)
    fssai_lic_number = serializers.CharField(required=False)
    fssai_lic_cert = serializers.FileField(required=False)
    fssai_start_date = serializers.DateField(required=False)
    fssai_end_date = serializers.DateField(required=False)
    gst_number = serializers.CharField(required=False)
    gst_cert = serializers.FileField(required=False)
    class Meta:
        model = models.Shop
        fields = '__all__'

    def create(self, validated_data):
        shop = models.Shop.objects.create(
            name = validated_data['name'],
            image = validated_data['image'],
            contact_number = validated_data['contact_number'],
            business_type = validated_data['business_type'],
            shop_type = validated_data['shop_type'],
            #indianrailways
            station = validated_data['station'],
            lat = validated_data['lat'],
            lon = validated_data['lon'],
            platform_a = validated_data['platform_a'],
            platform_b = validated_data['platform_b'],
            is_open = False,
            is_active = False,
            #payments
            is_cash = validated_data['is_cash'],
            is_card = validated_data['is_card'],
            is_upi = validated_data['is_upi']
        )
        shop.save()

        shop_license = models.ShopLicense.objects.create(
            shop = shop,
            registration = validated_data['lic_number'],
            certificate = validated_data['lic_cert'],
            start_date = validated_data['lic_start_date'],
            end_date = validated_data['lic_end_date'],
        )
        shop_license.save()

        try:
            shop_fssai_license = models.ShopFssaiLicense.objects.create(
                shop = shop,
                registration = validated_data['fssai_lic_number'],
                certificate = validated_data['fssai_lic_cert'],
                start_date = validated_data['fssai_start_date'],
                end_date = validated_data['fssai_end_date']
            )
            shop_fssai_license.save()
        except KeyError:
            pass
            
        try:
            shop_gst = models.ShopGst.objects.create(
                shop = shop,
                registration = validated_data['gst_number'],
                certificate = validated_data['gst_cert']
            )
            shop_gst.save()
        except KeyError:
            pass

        organization = OrgModel.Organization.objects.get(id=validated_data['organization'])
        organization_shop = models.OrganizationShop.objects.create(
            organization = organization,
            shop = shop
        )
        organization_shop.save()

        user = self.context.get('view').request.user
        organization_shop_employee = models.OrganizationShopEmployee.objects.create(
            organization = organization,
            shop = shop,
            user = user,
            is_manager = True,
            is_sales = True
        )
        organization_shop_employee.save()

        return shop


class ShopListSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Shop
        fields = ['id','name','image','station','platform_a','platform_b','is_open','is_active']


class OrganizationShopListSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Shop
        fields = ['id','name','image','station','platform_a','platform_b','is_open', 'is_active']


class PatchShopSerializer_iDukaan(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = ['id','contact_number','is_open','is_cash','is_card','is_upi']


class ShopDetailsSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    business_type = serializers.CharField()
    shop_type = serializers.CharField()
    class Meta:
        model = models.Shop
        exclude = ['created_at','updated_at','lat','lon']


class AddOrgShopEmpSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    empid = serializers.CharField()
    class Meta:
        model = models.OrganizationShopEmployee
        fields = ['id','empid','shop','is_manager','is_sales']

    def create(self, validated_data):
        org_emp = OrgModel.OrganizationEmployee.objects.get(id=validated_data['empid'])
        employee = models.OrganizationShopEmployee.objects.create(
            organization = org_emp.organization,
            user = org_emp.user,
            shop = validated_data['shop'],
            is_manager = validated_data['is_manager'],
            is_sales = validated_data['is_sales']
        )
        employee.save()
        return employee
    

class OrgShopEmpListSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    organization = serializers.SerializerMethodField()
    shop = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = models.OrganizationShopEmployee
        exclude = ['created_at','updated_at','user']
    
    def get_name(self, instance):
        user = UserModel.User.objects.get(username=instance.user)
        return f'{user.first_name} {user.last_name}'
    
    def get_organization(self, instance):
        return f'{instance.organization.id}'
    
    def get_shop(self, instance):
        return f'{instance.shop.id}' 


class UpdateOrgShopEmpSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = models.OrganizationShopEmployee
        fields = ['id','is_manager','is_sales']


