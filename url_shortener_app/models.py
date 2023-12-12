from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):
    verification_token = models.CharField(name="verification_token", max_length=100, null=False)
    verified = models.BooleanField(name="verified", default=False, null=False)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Users"
    
class UrlModel(models.Model):
    url = models.CharField(name="url", max_length=1000, null=False)
    short_url = models.CharField(name="short_url", max_length=10, null=False, unique=True)
    use_amount = models.IntegerField(name="use_amount", default=0)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.url
    
    class Meta:
        verbose_name_plural = "Urls"