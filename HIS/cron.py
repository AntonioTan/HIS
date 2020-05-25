from appoint.models import Doctor, Schedule, Department, Order
from login.models import User

def test():
    print('cronb test!')


def test1():
    new_doctor = Doctor.objects.create(name='test',
                                 sex=1,
                                 title='test',
                                 strength='test',
                                 department=Department.objects.all()[0],)
    new_doctor.save()


def restore_schedule():
    doctor_schedules = Schedule.objects.filter(type=1)
    normal_schedules = Schedule.objects.filter(type=0)
    for doctor_schedule in doctor_schedules:
        doctor_schedule.num = 30
    for normal_schedule in normal_schedules:
        normal_schedule.num = 100


def break_rule():
    orders = Order.objects.filter(status=2)
    for order in orders:
        order.status = 4





