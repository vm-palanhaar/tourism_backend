from django.db import models

class RailwayZone(models.Model):
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Zone Code')
    name = models.CharField(max_length=60, verbose_name='Zone')
    def __str__(self):
        return self.name

class RailwayDivision(models.Model):
    zone = models.ForeignKey(RailwayZone, on_delete=models.CASCADE, verbose_name='Railway Zone')
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Division Code')
    name = models.CharField(max_length=30,  verbose_name='Division')
    def __str__(self):
        return self.name

class RailwayStationCategoy(models.Model):
    category = models.CharField(max_length=6, verbose_name='Station Category', primary_key=True)
    def __str__(self):
        return self.category
    
class RailwayStation(models.Model):
    zone = models.ForeignKey(RailwayZone, on_delete=models.CASCADE, verbose_name='Railway Zone')
    division = models.ForeignKey(RailwayDivision, on_delete=models.CASCADE, verbose_name='Railway Division')
    category = models.ForeignKey(RailwayStationCategoy, on_delete=models.CASCADE, verbose_name='Railway Station Category')
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Station Code')
    name = models.CharField(max_length=30,  verbose_name='Railway Station')
    def __str__(self):
        return self.name
