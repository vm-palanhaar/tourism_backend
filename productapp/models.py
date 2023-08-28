from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Org(TimestampModel):
    name = models.CharField(max_length=60, verbose_name='Organization')
    address = models.TextField(verbose_name='Address')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    def __str__(self):
        return self.name


def upload_to_brand_image(instance,filename):
    brandname = instance.name
    return f'pc/{brandname}/{filename}' 

class Brand(TimestampModel):
    name = models.CharField(max_length=30, verbose_name='Brand')
    image = models.ImageField(_('Image'), upload_to=upload_to_brand_image)
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_show = models.BooleanField(default=True, verbose_name='Show Brand in Product Catalog')
    def __str__(self):
        return self.name
    

class OrgBrand(TimestampModel):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='orgbrand_org', verbose_name='Organization')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='orgbrand_brand', verbose_name='Brand')
    def __str__(self) -> str:
        return f'{self.org.name} - {self.brand.name}'


class ProdCat(models.Model):
    name = models.CharField(max_length=30, verbose_name='Category')
    desc = models.TextField(blank=True, verbose_name='Description')
    def __str__(self):
        return self.name
    
class ProdSubCat(models.Model):
    cat = models.ForeignKey(ProdCat, on_delete=models.CASCADE, related_name='prodsubcat_prodcat', verbose_name='Category')
    name = models.CharField(max_length=30, verbose_name='Subcategory')
    desc = models.TextField(blank=True, verbose_name='Description')
    def __str__(self):
        return self.name
    
class ProdMacroCat(models.Model):
    cat = models.ForeignKey(ProdCat, on_delete=models.CASCADE, related_name='prodmacrocat_prodcat', verbose_name='Category')
    sub_cat = models.ForeignKey(ProdSubCat, on_delete=models.CASCADE, related_name='prodmacrocat_prodsubcat', verbose_name='Subcategory')
    name = models.CharField(max_length=30, verbose_name='Macrocategory')
    desc = models.TextField(blank=True, verbose_name='Description')
    def __str__(self):
        return self.name
    

WEIGHT_CHOICES =( 
    ("g", "gram"), 
    ("kg", "kilogram "), 
    ("t", "tonne "), 
)
    

def upload_to_product_image_primary(instance,filename):
    productname = instance.name
    brandname = instance.brand.name
    return f'pc/{brandname}/{productname}/{filename}'

class Prod(TimestampModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='prod_brand', verbose_name='Brand')
    name = models.CharField(max_length=30, verbose_name='Product')
    price = models.DecimalField(decimal_places=2,max_digits=5, verbose_name='Price')
    desc = models.TextField(verbose_name='Description')
    image = models.ImageField(_('Image'), upload_to=upload_to_product_image_primary)
    weight = models.CharField(max_length=15, verbose_name='Weight', blank=True, null=True)
    net_weight = models.CharField(max_length=15, verbose_name='Net Weight', blank=True, null=True)
    # Category - Subcategory - Macrocategory
    cat = models.ForeignKey(ProdCat, on_delete=models.CASCADE, related_name='prod_prodcat', verbose_name='Category')
    sub_cat = models.ForeignKey(ProdSubCat, on_delete=models.CASCADE, related_name='prod_prodsubcat', verbose_name='Subcategory')
    macro_cat = models.ForeignKey(ProdMacroCat, on_delete=models.CASCADE, related_name='prod_prodmacrocat', verbose_name='Macrocategory')
    # Product Status
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_available = models.BooleanField(default=True, verbose_name='Availability')
    
    def __str__(self):
        return self.brand.name + ' ' + self.name


def upload_to_product_image(instance,filename):
    productname = instance.product.name
    brandname = instance.product.brand.name
    return f'pc/{brandname}/{productname}/{filename}'

class ProdImg(TimestampModel):
    prod = models.ForeignKey(Prod, default=None, on_delete=models.CASCADE, related_name='productimages')
    image = models.ImageField(_('Image'), upload_to=upload_to_product_image)
    def __str__(self):
        return self.prod.brand.name + ' ' + self.prod.name
