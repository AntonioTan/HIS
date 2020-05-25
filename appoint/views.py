from math import ceil

from django.shortcuts import render, redirect
from .models import Department, Doctor, Schedule, Order
from business_calendar import Calendar, MO, TU, WE, TH, FR
from datetime import datetime, timedelta
from django.views import View
from .forms import DatePickForm
from .data import appoint_basic_data
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HIS.settings")  # project_name 项目名称
django.setup()
from login.models import User


# Create your views here.
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
            context['date'] = str(datetime.today().date()+timedelta(days=kwargs['picked_date']))
            context['time'] = '上午8:00 --  10:00' if not kwargs['picked_morning_afternoon'] else '下午2:00 -- 4:00'
            context['schedule_id'] = schedule.id
            response = render(request, template_name='appoint/submit_test.html', context=context)
            response.set_cookie(key='user_id', value=request.COOKIES['user_id'], expires=3600)
            return response
        else:
            return render(request, 'login/home_page_test.html')
    else:
        if 'user_id' in request.COOKIES.keys():
            print(request.POST.get('description'))
            user_id = request.COOKIES.get('user_id')
            response = render(request, template_name='appoint/submit_test.html',)
            response.set_cookie(key='user_id', value=user_id, expires=3600)
            return response
        else:
            return render(request, 'login/home_page_test.html')


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
                    if 'picked_department_id' in self.initial.keys():
                        self.initial['schedule_objs'] = self.initial['schedule_objs'].filter(department=Department.objects.get(id=int(self.initial['picked_department_id'])))

                if key == 'picked_department_id':
                    self.initial['schedule_objs'] = Schedule.objects.filter(type=self.initial['picked_type'],
                                                                            morning_afternoon=self.initial['picked_morning_afternoon'],
                                                                            weekday=self.initial['picked_date'], department=Department.objects.get(id=self.initial['picked_department_id']))
            print(self.initial['picked_type']==0)
            if 'user_id' in request.COOKIES.keys():
                user_orders = Order.objects.filter(patient=User.objects.get(id=request.COOKIES['user_id']), status=2)
                print('GET User Order!')
                if user_orders:
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
                self.initial['page_schedules'] = self.initial['schedules'][(self.initial['picked_page']-1)*8: self.initial['picked_page']*8]
                self.initial['page_doctors'] = self.initial['doctors'][(self.initial['picked_page']-1)*8: self.initial['picked_page']*8]
            else:
                self.initial['page_schedules'] = self.initial['schedules'][
                    (self.initial['picked_page'] - 1) * 8:]
                self.initial['page_doctors'] = self.initial['doctors'][
                    (self.initial['picked_page'] - 1) * 8:]

            for key in self.initial.keys():
                if 'picked' in key:
                    print(key, self.initial[key])
            response = render(request, template_name='appoint/search_test.html', context=self.initial)
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
