from django.db import models
from userapp import models as UserModel

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class MobileApp(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    apk = models.CharField(max_length=30, blank=True, null=True, verbose_name='Android')
    ios = models.CharField(max_length=30, blank=True, null=True, verbose_name='iOS')

    def __str__(self):
        return self.name
    

class MobileAppFeedback(TimestampModel):
    app = models.ForeignKey(MobileApp, on_delete=models.CASCADE, verbose_name='App')
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE, verbose_name='User')
    subject = models.CharField(max_length=90, blank=True, null=True, verbose_name='Subject')
    comment = models.TextField(blank=True, verbose_name='Description')

    def __str__(self):
        return self.app.name
