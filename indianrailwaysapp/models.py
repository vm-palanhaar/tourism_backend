from django.utils.translation import gettext_lazy as _
from django.db import models

from businessapp import models as OrgModel
from userapp import models as UserModel
from productapp import models as PcModel

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
    

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    

class ShopType(models.Model):
    name = models.CharField(max_length=60, verbose_name='Name')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    def __str__(self):
        return self.name
    

class ShopBusinessType(models.Model):
    name = models.CharField(max_length=60, verbose_name='Name')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    shop_type = models.ManyToManyField(ShopType, related_name='shoptype')
    def __str__(self):
        return self.name
    

def upload_to_shop_image_primary(instance,filename):
    shopname = instance.name
    return f'business/shops/{shopname}/{filename}'

class Shop(TimestampModel):
    name = models.CharField(max_length=60, verbose_name='Shop Name')
    image = models.ImageField(_('Image'), upload_to=upload_to_shop_image_primary)
    contact_number = models.CharField(max_length=15, verbose_name='Contact Number')
    business_type = models.ForeignKey(ShopBusinessType, on_delete=models.CASCADE, verbose_name='Shop Business Type')
    shop_type = models.ForeignKey(ShopType, on_delete=models.CASCADE, verbose_name='Shop Type')
    #Indian Railways
    station = models.ForeignKey(RailwayStation, on_delete=models.CASCADE, verbose_name='Railway Station')
    lat = models.CharField(max_length=60, verbose_name='Latitdue')
    lon = models.CharField(max_length=60, verbose_name='Longitude')
    platform_a = models.CharField(max_length=15, blank=True, null=True, verbose_name='Primary Platform')
    platform_b = models.CharField(max_length=15, blank=True, null=True, verbose_name='Secondary Platform')
    is_open = models.BooleanField(default=False, verbose_name='Open')
    is_active = models.BooleanField(default=False, verbose_name='Verified')
    #Payment Methods
    is_cash = models.BooleanField(default=False, verbose_name='Cash')
    is_card = models.BooleanField(default=False, verbose_name='Card')
    is_upi = models.BooleanField(default=False, verbose_name='UPI')
    def __str__(self):
        return self.name
    

def upload_to_shop_license(instance,filename):
    shopname = instance.shop.name
    return f'business/shops/{shopname}/license/{filename}'
    
class ShopLicense(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    registration = models.CharField(max_length=30, verbose_name='License Number', unique=True)
    certificate = models.FileField(_('Document'), upload_to=upload_to_shop_license)
    start_date = models.DateField(blank=True, null=True, verbose_name='Start Date')
    end_date = models.DateField(blank=True, null=True, verbose_name='End Date')
    is_current = models.BooleanField(default=True, verbose_name='Current')
    def __str__(self):
        return self.shop.name


def upload_to_shop_fssai(instance,filename):
    shopname = instance.shop.name
    return f'business/shops/{shopname}/fssai/{filename}'

class ShopFssaiLicense(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    registration = models.CharField(max_length=30, verbose_name='FSSAI License Number')
    certificate = models.FileField(_('Document'), upload_to=upload_to_shop_fssai)
    start_date = models.DateField(blank=True, verbose_name='Start Date')
    end_date = models.DateField(blank=True, verbose_name='End Date')
    is_current = models.BooleanField(default=True, verbose_name='Current')
    def __str__(self):
        return self.shop.name
    

def upload_to_shop_gst(instance,filename):
    shopname = instance.shop.name
    return f'business/shops/{shopname}/gst/{filename}'

class ShopGst(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    registration = models.CharField(max_length=30, verbose_name='GST Number')
    certificate = models.FileField(_('Document'), upload_to=upload_to_shop_gst)
    is_current = models.BooleanField(default=True, verbose_name='Current')
    def __str__(self):
        return self.shop.name


class OrganizationShop(TimestampModel):
    organization = models.ForeignKey(OrgModel.Organization, on_delete=models.CASCADE, verbose_name='Organization')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop')


class OrganizationShopEmployee(TimestampModel):
    organization = models.ForeignKey(OrgModel.Organization, on_delete=models.CASCADE, verbose_name='Organization')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop')
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE, verbose_name='User')
    is_manager = models.BooleanField(default=False, verbose_name='Manager')
    is_sales = models.BooleanField(default=False, verbose_name='Sales')


class ShopInventory(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop')
    product = models.ForeignKey(PcModel.Product, on_delete=models.CASCADE, verbose_name='Product')
    is_stock = models.BooleanField(default=True, verbose_name='Stock')
