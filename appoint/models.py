from django.db import models

# Create your models here.


class Registration(models.Model):
    # type 1 for clinic || 0 for non-clinic
    type = models.BooleanField()
    # start_time will be used for checking whether this registration is valid
    # a registration is valid for 4 hour from start time
    start_time = models.DateTimeField()
    price = models.SmallIntegerField()
    doctor = models.ForeignKey(to='Doctor', on_delete=models.CASCADE)
    available = models.BooleanField()


class Department(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    # type 1 for check department || 0 for common department
    type = models.BooleanField()


class Doctor(models.Model):
    name = models.CharField(max_length=20, unique=True)
    # 1 for male || 0 for female
    sex = models.BooleanField()
    title = models.CharField(max_length=30)
    strength = models.CharField(max_length=50)
    department = models.ForeignKey(to='Department', on_delete=models.CASCADE)


class Order(models.Model):
    patient = models.ForeignKey(to='login.User', on_delete=models.CASCADE)
    registration = models.ForeignKey(to='Registration', on_delete=models.CASCADE)
    order_time = models.DateTimeField(null=True)
    # 1 for valid || 0 for invalid
    valid = models.BooleanField()


class Schedule(models.Model):
    doctor = models.ForeignKey(to='Doctor', on_delete=models.CASCADE)
    morning_registration_num = models.SmallIntegerField(default=0)
    afternoon_registration_num = models.SmallIntegerField(default=0)
    weekday = models.SmallIntegerField()
    # type 1 for clinic || 0 for non-clinic
    type = models.BooleanField()




