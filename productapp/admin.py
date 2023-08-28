from django.contrib import admin

from productapp import models

class OrgBrandAdmin(admin.TabularInline):
    model = models.OrgBrand
    extra = 0

@admin.register(models.Org)
class OrgConfig(admin.ModelAdmin):
    list_display = ['name','address','is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    inlines = [OrgBrandAdmin]

@admin.register(models.Brand)
class BrandConfig(admin.ModelAdmin):
    list_display = ['name','is_active','is_show']
    list_filter = ['is_active','is_show']
    search_fields = ['name']
    inlines = [OrgBrandAdmin]


class ProdSubCatAdmin(admin.TabularInline):
    model = models.ProdSubCat
    extra = 0

@admin.register(models.ProdCat)
class ProdCatConfig(admin.ModelAdmin):
    list_display = ['name','desc']
    search_fields = ['name']
    inlines = [ProdSubCatAdmin]

class ProdMacroCatAdmin(admin.TabularInline):
    model = models.ProdMacroCat
    extra = 0

@admin.register(models.ProdSubCat)
class ProdSubCatConfig(admin.ModelAdmin):
    list_display = ['name','cat','desc']
    search_fields = ['name']
    list_filter = ['cat']
    inlines = [ProdMacroCatAdmin]


class ProductImageAdmin(admin.TabularInline):
    model = models.ProdImg
    extra = 1

@admin.register(models.Prod)
class ProductConfig(admin.ModelAdmin):
    list_display = ['name','brand','price','cat','is_active','is_available']
    list_filter = ['is_active','is_available']
    search_fields = ['name','brand__name']
    raw_id_fields = ['brand','cat']
    inlines = [ProductImageAdmin]