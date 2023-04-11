from django.contrib import admin
from geographyapp import models

@admin.register(models.Country)
class CountryConfig(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','code','website','states')

    def states(self, obj):
        states = models.State.objects.filter(country=obj).count()
        return states


@admin.register(models.State)
class StateConfig(admin.ModelAdmin):
    search_fields = ['name','country__name']
    list_display = ('name','country','website')