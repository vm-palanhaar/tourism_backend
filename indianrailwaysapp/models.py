from django.utils.translation import gettext_lazy as _
from django.db import models

from businessapp import models as OrgModel
from userapp import models as UserModel
from productapp import models as PcModel
from geographyapp import models as GeoModel

class RailZone(models.Model):
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Zone Code')
    name = models.CharField(max_length=60, verbose_name='Zone')
    def __str__(self):
        return self.name

class RailDivision(models.Model):
    zone = models.ForeignKey(RailZone, on_delete=models.CASCADE, verbose_name='Railway Zone')
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Division Code')
    name = models.CharField(max_length=30,  verbose_name='Division')
    def __str__(self):
        return f'{self.name} - {self.zone.name}'

class RailStationCategoy(models.Model):
    category = models.CharField(max_length=6, verbose_name='Station Category', primary_key=True)
    def __str__(self):
        return self.category
    
class RailStation(models.Model):
    zone = models.ForeignKey(RailZone, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Railway Zone')
    div = models.ForeignKey(RailDivision, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Railway Division')
    cat = models.ForeignKey(RailStationCategoy, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Railway Station Category')
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Station Code')
    name = models.CharField(max_length=60,  verbose_name='Railway Station')
    platforms = models.CharField(max_length=15, blank=True, null=True, verbose_name='Platform')
    def __str__(self):
        return f'{self.name} - {self.code}'
    

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    

class ShopType(models.Model):
    name = models.CharField(max_length=60, verbose_name='Name', primary_key=True)
    desc = models.TextField(blank=True, null=True, verbose_name='Description')
    def __str__(self):
        return self.name
    

class ShopBusinessType(models.Model):
    name = models.CharField(max_length=60, verbose_name='Name', primary_key=True)
    desc = models.TextField(blank=True, null=True, verbose_name='Description')
    shop_type = models.ManyToManyField(ShopType, related_name='shoptypelist')
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
    station = models.ForeignKey(RailStation, on_delete=models.CASCADE, verbose_name='Railway Station')
    lat = models.CharField(max_length=15, verbose_name='Latitdue')
    lon = models.CharField(max_length=15, verbose_name='Longitude')
    platform_a = models.CharField(max_length=6, blank=True, null=True, verbose_name='Primary Platform')
    platform_b = models.CharField(max_length=6, blank=True, null=True, verbose_name='Secondary Platform')
    is_open = models.BooleanField(default=False, verbose_name='Open')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_verified = models.BooleanField(default=False, verbose_name='Verified')
    #Payment Methods
    is_cash = models.BooleanField(default=False, verbose_name='Cash')
    is_card = models.BooleanField(default=False, verbose_name='Card')
    is_upi = models.BooleanField(default=False, verbose_name='UPI')
    #Optional
    is_osop = models.BooleanField(default=False, verbose_name='OSOP Stall')
    is_baby = models.BooleanField(default=False, verbose_name='Baby Food')
    is_medical = models.BooleanField(default=False, verbose_name='OTC Medicine')
    def __str__(self):
        return f'{self.name}, {self.station.name} ({self.station.code})'
    

def upload_to_shop_license(instance,filename):
    shopname = instance.shop.name
    return f'business/shops/{shopname}/license/{filename}'
    
class ShopLic(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    reg_no = models.CharField(max_length=30, verbose_name='License Number', unique=True)
    doc = models.FileField(_('Document'), upload_to=upload_to_shop_license)
    start_date = models.DateField(blank=True, null=True, verbose_name='Start Date')
    end_date = models.DateField(blank=True, null=True, verbose_name='End Date')
    is_valid = models.BooleanField(default=False, verbose_name='Valid')
    def __str__(self):
        return self.shop.name


def upload_to_shop_fssai(instance,filename):
    shopname = instance.shop.name
    return f'business/shops/{shopname}/fssai/{filename}'

class ShopFssaiLic(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    reg_no = models.CharField(max_length=30, verbose_name='FSSAI License Number', unique=True)
    doc = models.FileField(_('Document'), upload_to=upload_to_shop_fssai)
    start_date = models.DateField(blank=True, verbose_name='Start Date')
    end_date = models.DateField(blank=True, verbose_name='End Date')
    is_current = models.BooleanField(default=True, verbose_name='Current')
    is_valid = models.BooleanField(default=False, verbose_name='Valid')
    def __str__(self):
        return self.shop.name
    

class ShopGst(TimestampModel):
    org = models.ForeignKey(OrgModel.Org, on_delete=models.CASCADE, verbose_name='Organization')
    gst = models.ForeignKey(OrgModel.OrgStateGstOps, on_delete=models.CASCADE, verbose_name='Organizaton-State')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    def __str__(self):
        return self.shop.name


class OrgShop(TimestampModel):
    org = models.ForeignKey(OrgModel.Org, on_delete=models.CASCADE, verbose_name='Organization')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop')


class OrgShopEmp(TimestampModel):
    org = models.ForeignKey(OrgModel.Org, on_delete=models.CASCADE, verbose_name='Organization')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop')
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE, verbose_name='User')
    is_manager = models.BooleanField(default=False, verbose_name='Manager')


class ShopInv(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop')
    product = models.ForeignKey(PcModel.Prod, on_delete=models.CASCADE, verbose_name='Product')
    is_stock = models.BooleanField(default=True, verbose_name='Stock')
    selling_price = models.DecimalField(blank=True, null=True, decimal_places=2,max_digits=5, verbose_name='Selling Price')


class IrHelplineNumber(models.Model):
    name = models.CharField(max_length=30, verbose_name="Name")
    state = models.ForeignKey(GeoModel.State, on_delete=models.CASCADE, blank=True, null=True, verbose_name='State')
    contact_number = models.CharField(max_length=15,verbose_name='Helpline Number')
    whatsapp = models.CharField(max_length=15, blank=True, null=True, verbose_name='WhatsApp')
    desc = models.TextField(verbose_name='Details', blank=True, null=True)

    def __str__(self):
        return self.contact_number


class Train(models.Model):
    train_no = models.IntegerField(verbose_name='Train No', primary_key=True)
    train_name = models.CharField(max_length=60, verbose_name='Train Name')
    station_from = models.ForeignKey(RailStation, on_delete=models.CASCADE, verbose_name='Station From', related_name='train_station_from')
    station_to = models.ForeignKey(RailStation, on_delete=models.CASCADE, verbose_name='Station To', related_name='train_station_to')
    run_sun = models.BooleanField(default=False, verbose_name='Train runs on Sunday')
    run_mon = models.BooleanField(default=False, verbose_name='Train runs on Monday')
    run_tue = models.BooleanField(default=False, verbose_name='Train runs on Tuesday')
    run_wed = models.BooleanField(default=False, verbose_name='Train runs on Wednesday')
    run_thu = models.BooleanField(default=False, verbose_name='Train runs on Thursday')
    run_fri = models.BooleanField(default=False, verbose_name='Train runs on Friday')
    run_sat = models.BooleanField(default=False, verbose_name='Train runs on Saturday')
    run_daily = models.BooleanField(default=False, verbose_name='Train runs Daily')
    duration = models.CharField(max_length=15, null=True, blank=True, verbose_name='Duration')
    def __str__(self):
        return f'{self.train_no} - {self.train_name}'


class TrainSchedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, verbose_name='Train')
    seq = models.IntegerField(verbose_name='Station No')
    day = models.IntegerField(verbose_name='Day')
    distance = models.IntegerField(verbose_name='Distance (in KM)')
    station = models.ForeignKey(RailStation, on_delete=models.CASCADE, verbose_name='Station')
    platform = models.CharField(max_length=6, blank=True, null=True, verbose_name='Platform')
    dep_time = models.TimeField(null=True, blank=True, verbose_name='Departure Time')
    arv_time = models.TimeField(null=True, blank=True, verbose_name='Arrival Time')
    halt_time = models.TimeField(null=True, blank=True, verbose_name='Halt Time')
    rev_dir = models.BooleanField(default=False, verbose_name='Reverse Direction')
    def __str__(self):
        return f'{self.station.name} - {self.station.code}'
