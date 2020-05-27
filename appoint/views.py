from math import ceil
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import Department, Doctor, Schedule, Order
from datetime import datetime, timedelta
from django.views import View
from .forms import DatePickForm
from .data import appoint_basic_data
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HIS.settings")  # project_name 项目名称
django.setup()
from login.models import User
from login.views import add_user_id


# Create your views here.
def admin_register(request, order_id):
    admin_template = 'appoint/admin.html'
    order = Order.objects.get(id=order_id)
    order.status = 3
    order.save()
    context = {}
    return render(request, template_name=admin_template, context=context)


def admin_search(request):
    admin_template = 'appoint/admin.html'
    user_name = request.POST['name']
    try:
        user = User.objects.get(name=user_name)
    except ObjectDoesNotExist:
        context = {'orders': []}
        context = add_user_id(request, context)
        context['error'] = ['用户名错误']
        return render(request, template_name=admin_template, context=context)
    hour_now = datetime.today().hour

    if 0 < hour_now < 10:
        morning_afternoon = 0
    elif 10 < hour_now < 24:
        morning_afternoon = 1
    else:
        morning_afternoon = -1
    if morning_afternoon == -1:
        context = {'orders': [],
                   'error': '此时间段不可签到'}
    else:
        today_date = datetime.today().date()
        today_start_datetime = datetime(year=today_date.year, month=today_date.month, day=today_date.day)
        today_end_datetime = datetime(year=today_date.year, month=today_date.month, day=today_date.day, hour=23)
        today_orders = Order.objects.filter(patient=user, order_time__range=(today_start_datetime, today_end_datetime), status=2)
        result_orders = []
        for today_order in today_orders:
            if today_order.registration.morning_afternoon == morning_afternoon:
                result_orders.append(today_order)
        context = {'orders': result_orders}
        if len(result_orders) == 0:
            context['error'] = '此时间段该用户没有预约'
    context = add_user_id(request, context)
    return render(request, template_name=admin_template, context=context)


def register_test(request, department, doctor_id, weekday, type):
    if len(str(department)) != 0:
        department = Department.objects.get(name=department)
        doctors = Doctor.objects.get(department=department)


def deal_date(request, picked_date):
    print(picked_date)
    return render(request, template_name='pay/index.html')


def deal_registration(request, *args, **kwargs):
    if request.method != 'POST':
        if 'user_id' in request.COOKIES.keys():
            print(kwargs)
            for key in kwargs.keys():
                kwargs[key] = int(kwargs[key])
            context = {}
            context = add_user_id(request, context)
            department = Department.objects.get(id=kwargs['picked_department_id'])
            if kwargs['picked_type']:
                doctor = Doctor.objects.get(id=kwargs['picked_doctor_id'])
                doctor = doctor
                schedule = Schedule.objects.get(department=department,
                                                           doctor=doctor,
                                                           morning_afternoon=kwargs['picked_morning_afternoon'],
                                                           type=kwargs['picked_type'],
                                                           weekday=kwargs['picked_date'],
                                                           )
                context['doctor_name'] = doctor.name
                context['doctor_sex'] = '男' if doctor.sex else '女'
                context['doctor_title'] = doctor.title
                context['doctor_strength'] = doctor.strength
            else:
                schedule = Schedule.objects.get(department=department,
                                                morning_afternoon=kwargs['picked_morning_afternoon'],
                                                type=kwargs['picked_type'],
                                                weekday=kwargs['picked_date'],
                                                           )
            context['department_name'] = department.name
            context['type'] = kwargs['picked_type']
            context['price'] = schedule.price
            if kwargs['picked_date'] - datetime.isoweekday(datetime.today()) < 0:
                kwargs['picked_date'] = 6+ kwargs['picked_date'] - datetime.isoweekday(datetime.today())
            else:
                kwargs['picked_date'] = kwargs['picked_date'] - datetime.isoweekday(datetime.today())
            print(kwargs['picked_date'])
            context['date'] = str(datetime.today().date()+timedelta(days=kwargs['picked_date']))
            context['time'] = '上午8:00 --  10:00' if not kwargs['picked_morning_afternoon'] else '下午2:00 -- 4:00'
            context['schedule_id'] = schedule.id
            response = render(request, template_name='appoint/submit.html', context=context)
            response.set_cookie(key='user_id', value=request.COOKIES['user_id'], expires=3600)
            return response
        else:
            return render(request, 'login/home_page.html')
    else:
        if 'user_id' in request.COOKIES.keys():
            print(request.POST.get('description'))
            user_id = request.COOKIES.get('user_id')
            response = render(request, template_name='appoint/submit.html')
            response.set_cookie(key='user_id', value=user_id, expires=3600)
            return response
        else:
            return render(request, 'login/home_page.html')


class AppointView(View):
    initial = appoint_basic_data
    form = DatePickForm()
    picked_data = {}

    def dispatch(self, request, *args, **kwargs):
        # self.initial['dates'] = [datetime.today().date() + timedelta(days=i) for i in range(7)]
        # self.initial['dates'] = [str(date) + weekdays[datetime.isoweekday(date)] for date in self.initial['dates']]
        print('dispatch')
        print(request.COOKIES)
        if request.method == 'POST':
            return self.post(request)
        else:
            for key in kwargs.keys():
                if key in ['picked_type','picked_page','picked_date','picked_morning_afternoon','picked_department_id']:
                    self.initial[key] = int(kwargs[key])
                else:
                    self.initial[key] = kwargs[key]

                if key in ['picked_type', 'picked_morning_afternoon', 'picked_date']:
                    self.initial['schedule_objs'] = Schedule.objects.filter(type=self.initial['picked_type'],
                                                                            morning_afternoon=self.initial['picked_morning_afternoon'],
                                                                            weekday=self.initial['picked_date'])
                    if 'picked_department_id' in self.initial.keys() and self.initial['picked_department_id'] != 0:
                        self.initial['schedule_objs'] = self.initial['schedule_objs'].filter(department=Department.objects.get(id=int(self.initial['picked_department_id'])))

                if key == 'picked_department_id'and self.initial['picked_department_id'] != 0:
                    self.initial['schedule_objs'] = Schedule.objects.filter(type=self.initial['picked_type'],
                                                                            morning_afternoon=self.initial['picked_morning_afternoon'],
                                                                            weekday=self.initial['picked_date'], department=Department.objects.get(id=self.initial['picked_department_id']))
                elif key == 'picked_department_id'and self.initial['picked_department_id'] == 0:
                    self.initial['schedule_objs'] = Schedule.objects.filter(type=self.initial['picked_type'],
                                                                            morning_afternoon=self.initial[
                                                                                'picked_morning_afternoon'],
                                                                            weekday=self.initial['picked_date'])
                else:
                    pass
            print(self.initial['picked_type']==0)
            if 'user_id' in request.COOKIES.keys():
                user_orders = Order.objects.filter(patient=User.objects.get(id=request.COOKIES['user_id']), status=2)
                if len(user_orders)!=0:
                    print('GET User Order!')
                    for user_order in user_orders:
                        print(user_order.id)
                        self.initial['schedule_objs'] = self.initial['schedule_objs'].exclude(id=user_order.registration.id)
            if self.initial['picked_type']:
                self.initial['doctor_objs'] = [schedule.doctor for schedule in self.initial['schedule_objs']]
                self.initial['pages'] = list(range(1, max(2, ceil(len(self.initial['doctor_objs'])/8+1))))
                self.initial['doctors'] = [{'id': doctor.id, 'name': doctor.name, 'sex': '男' if doctor.sex == 1 else '女',
                         'department_name': doctor.department.name, 'department_id': doctor.department.id, 'title': doctor.title} for doctor in
                        self.initial['doctor_objs']]
            else:
                self.initial['pages'] = list(range(1, max(2, ceil(len(self.initial['schedule_objs'])/8+1))))

            self.initial['schedules'] = [{'department_name': schedule.department.name, 'id': schedule.id, 'department_id': schedule.department.id} for schedule in
                              self.initial['schedule_objs']]

            if 'picked_page' not in kwargs.keys() and 'change_page' not in kwargs.keys():
                self.initial['picked_page'] = 1
            elif 'picked_page' in kwargs.keys():
                self.initial['picked_page'] = int(kwargs['picked_page'])
            elif kwargs['change_page']  == 'previous':
                self.initial['picked_page'] = self.initial['picked_page'] - 1 if  self.initial['picked_page'] != 1 else 1
            else:
                self.initial['picked_page'] = self.initial['picked_page'] + 1 if  self.initial['picked_page'] != self.initial['pages'][-1] else self.initial['pages'][-1]

            if self.initial['picked_page'] != self.initial['pages'][-1]:
                self.initial['page_schedules'] = self.initial['schedules'][(self.initial['picked_page']-1)*9: self.initial['picked_page']*9]
                self.initial['page_doctors'] = self.initial['doctors'][(self.initial['picked_page']-1)*9: self.initial['picked_page']*9]
            else:
                self.initial['page_schedules'] = self.initial['schedules'][
                    (self.initial['picked_page'] - 1) * 9:]
                self.initial['page_doctors'] = self.initial['doctors'][
                    (self.initial['picked_page'] - 1) * 9:]

            for key in self.initial.keys():
                if 'picked' in key:
                    print(key, self.initial[key])
            context = self.initial
            context = add_user_id(request, context)
            response = render(request, template_name='appoint/search.html', context=context)
            if 'user_id' in request.COOKIES.keys():
                response.set_cookie(key='user_id', value=request.COOKIES['user_id'], expires=3600)
            return response




    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         return self.post(request)
    #     else:
    #         return render(request, template_name='appoint/register_all_test.html', context={'days': self.form})
    #
    # def post(self, request, *args, **kwargs):
    #     self.initial = request.POST
    #     if 'dates' in self.initial.keys():
    #         today = datetime.today()
    #         picked_day = today + timedelta(days=int(self.initial['dates'][-1]))
    #         self.picked_data['date'] = picked_day
    #
    #     else:
    #         return render(request, template_name='appoint/register_all_test.html')
