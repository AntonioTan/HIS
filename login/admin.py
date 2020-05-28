from django.contrib import admin
from . import models

# Register your models here.
# I created a superuser
# username: tantianyi
# password: 123456
# with this superuser we can manage the backend
class UserAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'name']
    search_fields = ['id', 'name']


admin.site.register(models.User, UserAdmin)