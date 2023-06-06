from django.contrib import admin

from businessapp import models
from indianrailwaysapp import models as IrModel


@admin.register(models.OrgType)
class OrgTypeConfig(admin.ModelAdmin):
    list_display = ['entity','doc','verified','pending']

    def verified(self, instance):
        return models.Org.objects.filter(type=instance, is_active=True).count()
    
    def pending(self, instance):
        return models.Org.objects.filter(type=instance, is_active=False).count()


class OrgEmpAdmin(admin.TabularInline):
    model = models.OrgEmp
    extra = 0

class IrOrgShopAdmin(admin.TabularInline):
    model = IrModel.OrganizationShop
    extra = 0

class OrgStateGstOpsAdmin(admin.TabularInline):
    model = models.OrgStateGstOps
    extra = 0

@admin.register(models.Org)
class OrgConfig(admin.ModelAdmin):
    list_display = ['name','reg_no','type','is_active']
    list_filter = ['type','is_active']
    search_fields = ['name','reg_no']
    raw_id_fields = ['type']
    inlines = [OrgEmpAdmin,OrgStateGstOpsAdmin,IrOrgShopAdmin]
