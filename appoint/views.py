from django.shortcuts import render
from .models import Department, Doctor
from business_calendar import Calendar, MO, TU, WE, TH, FR
from datetime import datetime,timedelta
from django.views import View
from .forms import DatePickForm
from .data import appoint_basic_data
# Create your views here.


def register_test(request, department, doctor_id, weekday, type):
    if len(str(department)) != 0:
        department = Department.objects.get(name=department)
        doctors = Doctor.objects.get(department=department)


class AppointView(View):
    initial = appoint_basic_data
    form = DatePickForm()
    picked_data = {}

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request)
        else:
            return render(request, template_name='appoint/search_test.html', context=appoint_basic_data)


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


