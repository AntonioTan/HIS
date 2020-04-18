from django.contrib import admin
from . import models

# Register your models here.
# I created a superuser
# username: tantianyi
# password: 123456
# with this superuser we can manage the backend
admin.site.register(models.User)