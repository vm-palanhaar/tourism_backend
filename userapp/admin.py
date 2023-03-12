from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from businessapp import models as BusinessModel
from indianrailwaysapp import models as IrModel

class OrganizationEmployeeAdmin(admin.TabularInline):
    model = BusinessModel.OrganizationEmployee
    extra = 0

class OrganizationShopEmployeeAdmin(admin.TabularInline):
    model = IrModel.OrganizationShopEmployee
    extra = 0


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'username', 'first_name')
    list_filter = ['is_iDukaan','is_Yatrigan']
    list_display = ('email','username','first_name','last_name','contact_number')
    inlines = [OrganizationEmployeeAdmin, OrganizationShopEmployeeAdmin]

    fieldsets = (
        ('User Profile', {'fields': ('email','first_name','last_name','contact_number')}),
        ('Credentials', {'fields':('username','password')}),
        ('App Access',{'fields':('is_iDukaan', 'is_Yatrigan')}),
        ('User Type',{'fields':('is_active', 'is_staff','is_superuser')}),
    )

    add_fieldsets = (
        ('User Profile',{'classes':('wide',),
        'fields':('email','first_name','last_name','last_name','contact_number',)}),
        ('Credentials',{'classes':('wide',),
        'fields':('username','password','password2',)}),
        ('App Access',{'classes':('wide',),
        'fields':('is_iDukaan', 'is_Yatrigan')}),
        ('User Type',{'classes':('wide',),
        'fields':('is_active', 'is_staff','is_superuser')}),
    )

admin.site.register(User, UserAdminConfig)