from django.db import models
# Create your models here.


# class Registration(models.Model):
#     # type 1 for clinic || 0 for non-clinic
#     type = models.BooleanField()
#     # start_time will be used for checking whether this registration is valid
#     # a registration is valid for 4 hour from start time
#     start_time = models.DateTimeField()
#     price = models.SmallIntegerField()
#     doctor = models.ForeignKey(to='Doctor', on_delete=models.CASCADE)
#     available = models.BooleanField()


class Department(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    # type 1 for check department || 0 for common department
    type = models.BooleanField()

    def __unicode__(self):
        return self.name



class Doctor(models.Model):
    name = models.CharField(max_length=20, unique=True)
    # 1 for male || 0 for female
    sex = models.BooleanField()
    title = models.CharField(max_length=30)
    strength = models.CharField(max_length=50)
    department = models.ForeignKey(to='Department', on_delete=models.CASCADE)


class Order(models.Model):
    patient = models.ForeignKey(to='login.User', on_delete=models.CASCADE)
    registration = models.ForeignKey(to='Schedule', on_delete=models.CASCADE)
    order_time = models.DateField(null=True)
    # 1 for to_purchase || 2 for purchased || 3 for completed || 4 for against_rule
    status = models.SmallIntegerField(default=1)
    description = models.CharField(default='', max_length=300)


class Schedule(models.Model):
    doctor = models.ForeignKey(to='Doctor', on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(to='Department', on_delete=models.CASCADE)
    num = models.SmallIntegerField(default=0)
    # 0 for morning 1 for afternoon
    morning_afternoon = models.BooleanField(default=0)
    # 1 for Monday| 2 for Tuesday
    weekday = models.SmallIntegerField()
    # type 1 for doctor || 0 for non-doctor
    type = models.BooleanField()
    price = models.SmallIntegerField(default=80)

    def doctor_name(self):
        if self.type:
            return self.doctor.name
        else:
            return '无医生'
    doctor_name.short_description = 'Doctor Name'
    doctor_name.admin_order_field = 'doctor'

    def department_name(self):
        return self.department.name
    department_name.short_description = 'Department Name'
    department_name.admin_order_field = 'department'


class Report(models.Model):
    patient = models.ForeignKey(to='login.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    report_time = models.DateField()
    department = models.ForeignKey(to='Department', on_delete=models.CASCADE)
    result = models.TextField()
    note = models.TextField()

    def patient_name(self):
        return self.patient.name

    patient.short_description = 'Patient Name'





