from django.contrib import admin

from indianrailwaysapp import models

admin.site.register(models.RailwayZone)
admin.site.register(models.RailwayDivision)
admin.site.register(models.RailwayStationCategoy)
admin.site.register(models.RailwayStation)

admin.site.register(models.ShopType)
admin.site.register(models.ShopBusinessType)
admin.site.register(models.Shop)
admin.site.register(models.ShopLicense)
admin.site.register(models.ShopFssaiLicense)
admin.site.register(models.ShopGst)
admin.site.register(models.OrganizationShop)
admin.site.register(models.ShopInventory)
admin.site.register(models.OrganizationShopEmployee)
