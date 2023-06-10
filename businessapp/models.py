from django.utils.translation import gettext_lazy as _
from django.db import models

from userapp import models as UserModel
from geographyapp import models as GeoModel


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class OrgType(models.Model):
    entity = models.CharField(max_length=30, verbose_name='Entity')
    doc = models.CharField(max_length=30, verbose_name='Document')
    def __str__(self):
        return self.entity


def upload_to_organization(instance,filename):
    orgname = instance.name
    return f'business/org/{orgname}/{filename}'

class Org(TimestampModel):
    type = models.ForeignKey(OrgType, on_delete=models.CASCADE, verbose_name='Type')
    name = models.CharField(max_length=60, verbose_name='Name')
    reg_no = models.CharField(max_length=30, unique=True, verbose_name='Registration Number')
    doc = models.FileField(_('Document'), upload_to=upload_to_organization)
    is_active = models.BooleanField(default=False, verbose_name='Verified')
    def __str__(self):
        return self.name


class OrgEmp(TimestampModel):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Organization')
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE, verbose_name='User')
    is_manager = models.BooleanField(default=False, verbose_name='Manager')
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

def upload_to_org_gst(instance,filename):
    orgname = instance.org.name
    statename = instance.state.name
    return f'business/organization/{orgname}/gst/{statename}_{filename}'


class OrgStateGstOps(TimestampModel):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Organization')
    state = models.ForeignKey(GeoModel.State, on_delete=models.CASCADE, verbose_name='State')
    gstin = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name='GSTIN')
    doc = models.FileField(_('Document'), blank=True, null=True, upload_to=upload_to_org_gst)
    expiry = models.DateField(blank=True, null=True, verbose_name='Expiry Date')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_verified = models.BooleanField(default=False, verbose_name='Verified')
    def __str__(self):
        return self.state.name
