from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Country')
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Country Code')
    website = models.URLField(max_length=60, blank=True)
    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Country')
    name = models.CharField(max_length=30, verbose_name='State')
    website = models.URLField(max_length=60, blank=True)
    def __str__(self):
        return self.name
