from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    # DateField uses datetime.date
    # datetime.date year month day
    birth = models.DateField()
    # calculate age from birth
    age = models.SmallIntegerField()
    # 1 for male || 0 for female
    sex = models.BooleanField()
    # phone number
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    # save the date&time when a user successfully signs up
    sign_up_time = models.DateTimeField()
    # TODO Here we need to define the max appointment time a user can have
    # I suppose a user can only make 3 appointments a day?
    appoint_times = models.SmallIntegerField()
    # This can be defined according to appoint_times
    appoint_available = models.BooleanField()
    # break rule times
    break_rule_times = models.SmallIntegerField(default=0)
    # 0 for non-admin| 1 for admin
    admin = models.BooleanField(default=0)

    def __str__(self):
        return self.name