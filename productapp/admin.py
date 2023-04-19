from django.contrib import admin

from productapp import models

class ProductGroupAdmin(admin.TabularInline):
    model = models.ProductGroup
    extra = 1

@admin.register(models.Brand)
class BrandConfig(admin.ModelAdmin):
    list_display = ['name','is_active','is_show']
    list_filter = ['is_active','is_show']
    search_fields = ['name']
    inlines = [ProductGroupAdmin]

class ProductSubGroupAdmin(admin.TabularInline):
    model = models.ProductSubGroup
    extra = 1

@admin.register(models.ProductGroup)
class ProductGroupConfig(admin.ModelAdmin):
    list_display = ['name','brand']
    search_fields = ['name']
    inlines = [ProductSubGroupAdmin]

class ProductImageAdmin(admin.TabularInline):
    model = models.ProductImage
    extra = 1

admin.site.register(models.ProductCategory)

@admin.register(models.Product)
class ProductConfig(admin.ModelAdmin):
    list_display = ['name','brand','price','category','is_active','is_available']
    list_filter = ['is_active','is_available']
    search_fields = ['name','brand__name']
    raw_id_fields = ['brand','category']
    inlines = [ProductImageAdmin]

admin.site.register(models.ProductSubGroup)
