from django.contrib import admin
from . import models
# Register your models here.
# admin.site.register(models.Registration)


class DoctorAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['title']


class DepartmentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'name']
    list_filter = ['name']

admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Order)


class ScheduleAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ['type', 'weekday']
    search_fields = ['id', 'doctor_name', 'department_name']
    list_display = ('id', 'doctor_name', 'department_name', 'num', 'weekday')

admin.site.register(models.Schedule, ScheduleAdmin)
admin.site.register(models.Report)