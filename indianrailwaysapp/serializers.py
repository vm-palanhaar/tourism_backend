from rest_framework import serializers
from datetime import date

from indianrailwaysapp import models
from userapp import models as UserModel
from productapp import serializers as PcSerializer
from businessapp import models as OrgModel
from businessapp import serializers as OrgSerializer

'''
Common APIs Serializer
1. RailStationList
2. ShopInvList
3. IrHelplineNumberList
4. IrGRPList

Yatrigan APIs Serializer
1. ShopList_Yatrigan
2. ShopInfo_Yatrigan
3. TrainList_Yatrigan
4. TrainSchedule_Yatrigan

iDukaan APIs Serializer
1. ShopBusinessTypeList_iDukaan
2. AddShop_iDukaan
3. ShopList_iDukaan
4. OrgShopList_iDukaan
5. UpdateShop_iDukaan
6. ShopInfo_iDukaan
7. AddOrgShopEmp_iDukaan
8. OrgShopEmpList_iDukaan
9. UpdateOrgShopEmp_iDukaan
10. AddShopLic_iDukaan
11. ShopLicList_iDukaan
12. AddShopFssaiLic_iDukaan
13. ShopFssaiLicList_iDukaan
14. AddShopInv_iDukaan
15. PatchShopInv_iDukaan
16. AddShopGst_iDukaan
17. ShopGstList_iDukaan

'''

class RailStationList(serializers.ModelSerializer):
    station = serializers.SerializerMethodField()
    class Meta:
        model = models.RailStation
        fields = ['station']

    def get_station(self, instance):
        return f'{instance.name} - {instance.code}'


class ShopInvList(serializers.ModelSerializer):
    id = serializers.CharField()
    product= serializers.SerializerMethodField()
    class Meta:
        model = models.ShopInv
        exclude = ['created_at','updated_at','shop','is_stock']

    def get_product(self, instance):
        return PcSerializer.ProductListSerializer(instance.product).data


class IrHelplineNumberList(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.IrHelplineNumber
        fields = ['id','contact_number','whatsapp','desc','name']


class IrGRPList(serializers.ModelSerializer):
    id = serializers.CharField()
    state = serializers.CharField()
    class Meta:
        model = models.IrHelplineNumber
        fields = '__all__'


class ShopList_Yatrigan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Shop
        fields = ['id','name','image','platform_a','platform_b','is_baby','is_medical']


class ShopInfo_Yatrigan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Shop
        fields = ['id','name','image','contact_number','station','platform_a','platform_b','is_cash','is_card','is_upi']


class ShopBusinessTypeList_iDukaan(serializers.ModelSerializer):
    class Meta:
        model = models.ShopBusinessType
        fields = '__all__'


class AddShop_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True)
    contact_number = serializers.CharField(write_only=True)
    lat = serializers.CharField(write_only=True)
    lon = serializers.CharField(write_only=True)
    platform_a = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    platform_b = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    is_cash = serializers.BooleanField(write_only=True)
    is_card = serializers.BooleanField(write_only=True)
    is_upi = serializers.BooleanField(write_only=True)
    is_baby = serializers.BooleanField(write_only=True)
    is_medical = serializers.BooleanField(write_only=True)
    org = serializers.CharField(required=True, write_only=True)
    lic_number = serializers.CharField(required=True, write_only=True)
    lic_doc = serializers.FileField(required=True, write_only=True)
    lic_start_date = serializers.DateField(required=True, write_only=True)
    lic_end_date = serializers.DateField(required=True, write_only=True)
    class Meta:
        model = models.Shop
        exclude = ['created_at','updated_at','is_open','is_active']

    def create(self, validated_data):
        today_date = date.today()
        is_active = today_date < validated_data['lic_end_date']
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
            is_active = is_active,
            is_verified = False,
            #payments
            is_cash = validated_data['is_cash'],
            is_card = validated_data['is_card'],
            is_upi = validated_data['is_upi'],
            #option
            is_osop = validated_data['is_osop'],
            is_baby = validated_data['is_baby'],
            is_medical = validated_data['is_medical']
        )

        shopLic = models.ShopLic.objects.create(
            shop = shop,
            reg_no = validated_data['lic_number'],
            doc = validated_data['lic_doc'],
            start_date = validated_data['lic_start_date'],
            end_date = validated_data['lic_end_date'],
            is_valid = False
        )
        shopLic.save()

        org = OrgModel.Org.objects.get(id=validated_data['org'])
        orgShop = models.OrgShop.objects.create(
            org = org,
            shop = shop
        )
        orgShop.save()

        orgShopEmp = models.OrgShopEmp.objects.create(
            org = org,
            shop = shop,
            user = self.context.get('user'),
            is_manager = True
        )
        orgShopEmp.save()

        shop.save()

        return shop


class ShopList_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Shop
        fields = ['id','name','image','station','platform_a','platform_b','is_open','is_active','is_verified','is_baby','is_medical']


class OrgShopList_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Shop
        fields = ['id','name','image','station','platform_a','platform_b','is_open', 'is_active','is_verified','is_baby','is_medical']


class UpdateShop_iDukaan(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = ['id','contact_number','is_open','is_cash','is_card','is_upi']


class ShopInfo_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    business_type = serializers.CharField()
    shop_type = serializers.CharField()
    class Meta:
        model = models.Shop
        exclude = ['created_at','updated_at','lat','lon']


class AddOrgShopEmp_iDukaan(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    user = serializers.CharField(required=False, read_only=True)
    empId = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = models.OrgShopEmp
        fields = ['id','empId','shop','is_manager','user']

    def create(self, validated_data):
        org_emp = OrgModel.OrgEmp.objects.get(id=validated_data['empId'])
        employee = models.OrgShopEmp.objects.create(
            org = org_emp.org,
            user = org_emp.user,
            shop = validated_data['shop'],
            is_manager = validated_data['is_manager'],
        )
        employee.save()
        return employee
    

class OrgShopEmpList_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = models.OrgShopEmp
        exclude = ['created_at','updated_at','user','org','shop']
    
    def get_name(self, instance):
        return f'{instance.user.first_name} {instance.user.last_name}'


class UpdateOrgShopEmp_iDukaan(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = models.OrgShopEmp
        fields = ['id','is_manager']


class AddShopLic_iDukaan(serializers.ModelSerializer):
    doc = serializers.FileField(write_only=True)
    class Meta:
        model = models.ShopLic
        exclude = ['created_at','updated_at','is_valid']


class ShopLicList_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    docType = serializers.SerializerMethodField()
    class Meta:
        model = models.ShopLic
        exclude = ['created_at','updated_at','doc','shop']

    def get_docType(self,instance):
        if instance.end_date == None:
            return 'Notice'
        return 'License'
    

class AddShopFssaiLic_iDukaan(serializers.ModelSerializer):
    doc = serializers.FileField(write_only=True)
    class Meta:
        model = models.ShopFssaiLic
        exclude = ['created_at','updated_at','is_current','is_valid']


class ShopFssaiLicList_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.ShopFssaiLic
        exclude = ['created_at','updated_at','doc','shop']


class AddShopInv_iDukaan(serializers.ModelSerializer):
    class Meta:
        model = models.ShopInv
        exclude = ['created_at','updated_at','is_stock']


class PatchShopInv_iDukaan(serializers.ModelSerializer):
    class Meta:
        model = models.ShopInv
        fields = ['id','is_stock','selling_price']


class AddShopGst_iDukaan(serializers.ModelSerializer):
    class Meta:
        model = models.ShopGst
        exclude = ['created_at','updated_at']


class ShopGstList_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    gst = OrgSerializer.OrgStateGstOpsListSerializer()
    class Meta:
        model = models.ShopGst
        exclude = ['created_at','updated_at']
    

class TrainList_Yatrigan(serializers.ModelSerializer):
    train = serializers.SerializerMethodField()
    class Meta:
        model = models.Train
        fields = ['train']

    def get_train(self, instance):
        return f'{instance.train_no} - {instance.train_name}'


class _TrainScheduleStationList(serializers.ModelSerializer):
    station = serializers.SerializerMethodField()
    class Meta:
        model = models.TrainSchedule
        exclude = ['id','seq','train']
    
    def get_station(self, instance):
        return f'{instance.station.name} - {instance.station.code}'
    

class TrainSchedule_Yatrigan(serializers.ModelSerializer):
    station_from = serializers.SerializerMethodField()
    station_to = serializers.SerializerMethodField()
    stations = serializers.SerializerMethodField()
    run_status = serializers.SerializerMethodField()
    class Meta:
        model = models.Train
        fields = ['train_no','train_name','station_from','station_to'
                  ,'stations','run_status','duration']
        
    def get_station_from(self, instance):
        return f'{instance.station_from.name} - {instance.station_from.code}'
    
    def get_station_to(self, instance):
        return f'{instance.station_to.name} - {instance.station_from.code}'

    def get_stations(self, instance):
        schedule = models.TrainSchedule.objects.filter(train=instance)
        serializer = _TrainScheduleStationList(schedule, many=True)
        return serializer.data
    
    def get_run_status(self, instance):
        days = []
        if instance.run_sun:
            days.append('SUN')
        if instance.run_mon:
            days.append('MON')
        if instance.run_tue:
            days.append('TUE')
        if instance.run_wed:
            days.append('WED')
        if instance.run_thu:
            days.append('THU')
        if instance.run_fri:
            days.append('FRi')
        if instance.run_sat:
            days.append('SAT')
        return days

