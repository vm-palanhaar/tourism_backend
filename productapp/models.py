from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


def upload_to_brand_image(instance,filename):
    brandname = instance.name
    return f'productcatalog/{brandname}/{filename}' 

class Brand(TimestampModel):
    name = models.CharField(max_length=30, verbose_name='Brand')
    image = models.FileField(_('Image'), upload_to=upload_to_brand_image, null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_show = models.BooleanField(default=True, verbose_name='Show Brand in Product Catalog')
    def __str__(self):
        return self.name
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name='Category')
    description = models.TextField(blank=True, verbose_name='Description')
    def __str__(self):
        return self.name
    

def upload_to_product_image_primary(instance,filename):
    productname = instance.name
    brandname = instance.brand.name
    return f'productcatalog/{brandname}/{productname}/{filename}'

class Product(TimestampModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='productbrandprod', verbose_name='Brand')
    name = models.CharField(max_length=30, verbose_name='Product')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    price = models.DecimalField(decimal_places=2,max_digits=5, verbose_name='Price')
    weight = models.CharField(max_length=15, verbose_name='Net Weight')
    image = models.ImageField(_('Image'), upload_to=upload_to_product_image_primary)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='productcatagoryprod', verbose_name='Category')
    is_active = models.BooleanField(default=False, verbose_name='Verified')
    is_available = models.BooleanField(default=True, verbose_name='Availability')
    
    def __str__(self):
        return self.brand.name + ' ' + self.name


def upload_to_product_image(instance,filename):
    productname = instance.product.name
    brandname = instance.product.brand.name
    return f'productcatalog/{brandname}/{productname}/{filename}'

class ProductImage(TimestampModel):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='productimages')
    image = models.ImageField(_('Image'), upload_to=upload_to_product_image)
    def __str__(self):
        return self.product.brand.name + ' ' + self.product.name


class ProductGroup(models.Model):
    name = models.CharField(max_length=30, verbose_name='Group')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='groupbrandprod', verbose_name='Brand')
    def __str__(self):
        return f'{self.brand.name} ({self.name})'
    
class ProductSubGroup(models.Model):
    group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name='subgroupbrandprod', verbose_name='Group')
    name = models.CharField(max_length=30, verbose_name='Sub-Group')
    products = models.ManyToManyField(Product, null=True, blank=True)
    def __str__(self):
        return self.name
