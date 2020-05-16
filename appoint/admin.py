from django.contrib import admin
from . import models
# Register your models here.
# admin.site.register(models.Registration)
admin.site.register(models.Department)
admin.site.register(models.Doctor)
admin.site.register(models.Order)
admin.site.register(models.Schedule)