from django.contrib import admin

from indianrailwaysapp import models


#Indian Railways Zone, Division, Station

class RailwayDivisionAdmin(admin.TabularInline):
    model = models.RailDivision
    extra = 0

@admin.register(models.RailZone)
class RailwayZoneConfig(admin.ModelAdmin):
    list_display = ('code','name','divisions','railway_stations')
    inlines = [RailwayDivisionAdmin]

    def divisions(self, obj):
        divisions = models.RailDivision.objects.filter(zone=obj).count()
        return divisions

    def railway_stations(self, obj):
        railwaystations = models.RailStation.objects.filter(zone=obj).count()
        return railwaystations


class RailwayStationAdmin(admin.TabularInline):
    model = models.RailStation
    extra = 0

@admin.register(models.RailDivision)
class RailwayDivisionConfig(admin.ModelAdmin):
    search_fields = ['zone__name','name']
    list_display = ('name','zone','railway_stations')
    inlines = [RailwayStationAdmin]

    def railway_stations(self, obj):
        railwaystations = models.RailStation.objects.filter(div=obj).count()
        return railwaystations
    

admin.site.register(models.RailStationCategoy)

class ShopAdmin(admin.TabularInline):
    model = models.Shop
    fields = ['name','platform_a','platform_b','is_open','is_active']
    extra = 0


@admin.register(models.RailStation)
class RailwayStationConfig(admin.ModelAdmin):
    search_fields = ['code','name','zone__name','div__name']
    list_display = ('code','name','div','zone')
    fieldsets = (
        ('Railway Station', {'fields':('zone','div','code','name','cat')}),
    )
    inlines = [ShopAdmin]


#Indian Railways Commerial

admin.site.register(models.ShopType)
admin.site.register(models.ShopBusinessType)

class OrganizationShopAdmin(admin.TabularInline):
    model = models.OrgShop
    extra = 0

class ShopLicenseAdmin(admin.TabularInline):
    model = models.ShopLic
    extra = 0

class ShopFssaiLicenseAdmin(admin.TabularInline):
    model = models.ShopFssaiLic
    extra = 0

class ShopGstAdmin(admin.TabularInline):
    model = models.ShopGst
    extra = 0

class ShopInventoryAdmin(admin.TabularInline):
    model = models.ShopInv
    extra = 0

class OrganizationShopEmployeeAdmin(admin.TabularInline):
    model = models.OrgShopEmp
    extra = 0

@admin.register(models.Shop)
class ShopConfig(admin.ModelAdmin):
    fieldsets = (
        ('SHOP', {'fields':('name','image','contact_number','business_type','shop_type')}),
        ('INDIAN RAILWAYS', {'fields':('lat','lon','station','platform_a','platform_b')}),
        ('PAYMENT', {'fields':('is_cash','is_card','is_upi')}),
        ('STATUS', {'fields':('is_open','is_active','is_verified')}),
    )
    raw_id_fields = ['station']
    inlines = [OrganizationShopAdmin,ShopLicenseAdmin,ShopFssaiLicenseAdmin,
               ShopGstAdmin,ShopInventoryAdmin,OrganizationShopEmployeeAdmin]   


# Helpine Numbers
admin.site.register(models.IrHelplineNumber)

class TrainScheduleAdmin(admin.TabularInline):
    model = models.TrainSchedule
    raw_id_fields = ['station']
    extra = 0

@admin.register(models.Train)
class TrainConfig(admin.ModelAdmin):
    fieldsets = (
        ('TRAIN', {'fields':('train_no','train_name')}),
        ('STATION', {'fields':('station_from','station_to','duration')}),
        ('RUN', {'fields':('run_sun','run_mon','run_tue','run_wed','run_thu','run_fri','run_sat','run_daily')}),
    )
    raw_id_fields = ['station_from','station_to']
    inlines = [TrainScheduleAdmin]
