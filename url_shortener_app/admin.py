from django.contrib import admin
from .models import UserModel, UrlModel
# Register your models here.

admin.site.register(UserModel)
admin.site.register(UrlModel)