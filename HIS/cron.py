from appoint.models import Doctor, Schedule, Department, Order
from login.models import User
from datetime import datetime

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
    print('restore_schedule')
    doctor_schedules = Schedule.objects.filter(type=1)
    normal_schedules = Schedule.objects.filter(type=0)
    for doctor_schedule in doctor_schedules:
        doctor_schedule.num = 30
    for normal_schedule in normal_schedules:
        normal_schedule.num = 100


def break_rule():
    print('break_rule')
    orders = Order.objects.filter(status=2, order_time=datetime.today())
    for order in orders:
        order.status = 4
        order.save()


def restore_user():
    print('restore_user')
    users = User.objects.all()
    for user in users:
        if user.admin == 0:
            user_break_orders = Order.objects.filter(patient=user, status=4)
            if len(user_break_orders):
                user.appoint_available = False
                user.appoint_times = 0
                user.save()
            else:
                user.appoint_times = 3
                user.appoint_available = True
                user.save()




