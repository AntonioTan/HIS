from django.shortcuts import render, redirect
from .models import Department, Doctor, Schedule
from business_calendar import Calendar, MO, TU, WE, TH, FR
from datetime import datetime, timedelta
from django.views import View
from .forms import DatePickForm
from .data import appoint_basic_data


# Create your views here.


def register_test(request, department, doctor_id, weekday, type):
    if len(str(department)) != 0:
        department = Department.objects.get(name=department)
        doctors = Doctor.objects.get(department=department)


def deal_date(request, picked_date):
    print(picked_date)
    return render(request, template_name='appoint/search_test.html')


class AppointView(View):
    initial = appoint_basic_data
    form = DatePickForm()
    picked_data = {}

    def dispatch(self, request, *args, **kwargs):
        # self.initial['dates'] = [datetime.today().date() + timedelta(days=i) for i in range(7)]
        # self.initial['dates'] = [str(date) + weekdays[datetime.isoweekday(date)] for date in self.initial['dates']]
        print('dispatch')
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
            if self.initial['picked_type']:
                self.initial['doctor_objs'] = [schedule.doctor for schedule in self.initial['schedule_objs']]
                self.initial['doctors'] = [{'id': doctor.id, 'name': doctor.name, 'sex': '男' if doctor.sex == 1 else '女',
                         'department_name': doctor.department.name, 'title': doctor.title} for doctor in
                        self.initial['doctor_objs']]
            self.initial['schedules'] = [{'department_name': schedule.department.name, 'id': schedule.id} for schedule in
                              self.initial['schedule_objs']]

            for key in self.initial.keys():
                if 'picked' in key:
                    print(key, self.initial[key])
            return render(request, template_name='appoint/search_test.html', context=self.initial)



    #
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
