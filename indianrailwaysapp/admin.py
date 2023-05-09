from django.contrib import admin

from indianrailwaysapp import models


#Indian Railways Zone, Division, Station

class RailwayDivisionAdmin(admin.TabularInline):
    model = models.RailwayDivision
    extra = 0

@admin.register(models.RailwayZone)
class RailwayZoneConfig(admin.ModelAdmin):
    list_display = ('code','name','divisions','railway_stations')
    inlines = [RailwayDivisionAdmin]

    def divisions(self, obj):
        divisions = models.RailwayDivision.objects.filter(zone=obj).count()
        return divisions

    def railway_stations(self, obj):
        railwaystations = models.RailwayStation.objects.filter(zone=obj).count()
        return railwaystations


class RailwayStationAdmin(admin.TabularInline):
    model = models.RailwayStation
    extra = 0

@admin.register(models.RailwayDivision)
class RailwayDivisionConfig(admin.ModelAdmin):
    search_fields = ['zone__name','name']
    list_display = ('name','zone','railway_stations')
    inlines = [RailwayStationAdmin]

    def railway_stations(self, obj):
        railwaystations = models.RailwayStation.objects.filter(division=obj).count()
        return railwaystations
    

admin.site.register(models.RailwayStationCategoy)

class ShopAdmin(admin.TabularInline):
    model = models.Shop
    fields = ['name','platform_a','platform_b','is_open','is_active']
    extra = 0

@admin.register(models.RailwayStation)
class RailwayStationConfig(admin.ModelAdmin):
    search_fields = ['code','name','zone__name','division__name']
    list_display = ('code','name','division','zone')
    fieldsets = (
        ('Railway Station', {'fields':('zone','division','code','name','category')}),
    )
    inlines = [ShopAdmin]


#Indian Railways Commerial

admin.site.register(models.ShopType)
admin.site.register(models.ShopBusinessType)

class OrganizationShopAdmin(admin.TabularInline):
    model = models.OrganizationShop
    extra = 0

class ShopLicenseAdmin(admin.TabularInline):
    model = models.ShopLicense
    extra = 0

class ShopFssaiLicenseAdmin(admin.TabularInline):
    model = models.ShopFssaiLicense
    extra = 0

class ShopGstAdmin(admin.TabularInline):
    model = models.ShopGst
    extra = 0

class ShopInventoryAdmin(admin.TabularInline):
    model = models.ShopInventory
    extra = 0

class OrganizationShopEmployeeAdmin(admin.TabularInline):
    model = models.OrganizationShopEmployee
    extra = 0

@admin.register(models.Shop)
class ShopConfig(admin.ModelAdmin):
    fieldsets = (
        ('SHOP', {'fields':('name','image','contact_number','business_type','shop_type')}),
        ('INDIAN RAILWAYS', {'fields':('lat','lon','station','platform_a','platform_b')}),
        ('PAYMENT', {'fields':('is_cash','is_card','is_upi')}),
        ('STATUS', {'fields':('is_open','is_active')}),
    )
    inlines = [OrganizationShopAdmin,ShopLicenseAdmin,ShopFssaiLicenseAdmin,
               ShopGstAdmin,ShopInventoryAdmin,OrganizationShopEmployeeAdmin]   


# Helpine Numbers

admin.site.register(models.IrGRP)
admin.site.register(models.Train)
admin.site.register(models.TrainSchedule)
