from django.contrib import admin

from businessapp import models


@admin.register(models.OrganizationType)
class OrganizationTypeConfig(admin.ModelAdmin):
    list_display = ['entity','document','verified','pending']

    def verified(self, instance):
        return models.Organization.objects.filter(entity=instance, is_active=True).count()
    
    def pending(self, instance):
        return models.Organization.objects.filter(entity=instance, is_active=False).count()


class OrganizationEmployeeAdmin(admin.TabularInline):
    model = models.OrganizationEmployee
    extra = 1

@admin.register(models.Organization)
class OrganizationConfig(admin.ModelAdmin):
    list_display = ['name','registration','entity','is_active']
    list_filter = ['entity','is_active']
    search_fields = ['name','registration']
    raw_id_fields = ['entity']
    inlines = [OrganizationEmployeeAdmin]
