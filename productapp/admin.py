from django.contrib import admin

from productapp import models


@admin.register(models.Brand)
class BrandConfig(admin.ModelAdmin):
    list_display = ['name','is_active','is_show']
    list_filter = ['is_active','is_show']
    search_fields = ['name']

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
