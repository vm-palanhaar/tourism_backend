from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, last_name, contact_number, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_iDukaan', True)
        other_fields.setdefault('is_Yatrigan', True)
        return self.create_user(email, username, first_name, last_name, contact_number, password, **other_fields)

    def create_user(self, email, username, first_name, last_name, contact_number, password=None, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, contact_number=contact_number, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email')
    username = models.CharField(max_length=60, verbose_name='Username', primary_key=True)
    first_name = models.CharField(max_length=60, verbose_name='First Name')
    last_name = models.CharField(max_length=60, verbose_name='Last Name')
    contact_number = models.CharField(max_length=10,verbose_name='Mobile Number')

    is_iDukaan = models.BooleanField(default=False, verbose_name='iDukaan')
    is_Yatrigan = models.BooleanField(default=False, verbose_name='Yatrigan')

    otp = models.CharField(max_length=6, verbose_name='OTP', blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name='Account Status')
    is_staff = models.BooleanField(default=False, verbose_name='Palanhaar Staff')
    is_superuser = models.BooleanField(default=False, verbose_name='Palanhaar Admin')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'contact_number']

    def __str__(self):
        return self.username