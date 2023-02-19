from django.utils.translation import gettext_lazy as _
from django.db import models

from userapp import models as UserModel


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class OrganizationType(models.Model):
    entity = models.CharField(max_length=30, verbose_name='Entity')
    document = models.CharField(max_length=30, verbose_name='Document')
    def __str__(self):
        return self.entity


def upload_to_organization(instance,filename):
    organizationname = instance.name
    return f'business/organization/{organizationname}/{filename}'

class Organization(TimestampModel):
    entity = models.ForeignKey(OrganizationType, on_delete=models.CASCADE, verbose_name='Entity')
    name = models.CharField(max_length=60, verbose_name='Name')
    registration = models.CharField(max_length=30, unique=True, verbose_name='Document Number')
    document = models.FileField(_('Document'), upload_to=upload_to_organization)
    is_active = models.BooleanField(default=False, verbose_name='Verified')
    def __str__(self):
        return self.name


class OrganizationEmployee(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Organization')
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE, verbose_name='Employee')
    manager = models.BooleanField(default=False, verbose_name='Manager')
    def __str__(self):
        return self.organization.name
