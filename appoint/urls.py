from django.urls import path, re_path
from . import views

app_name = 'appoint'
patterns = [
    re_path(r'^register_test/department=(?P<department>\w+)/doctor_id=(?P<doctor_id>\d+)/weekday=(?P<weekday>\d)/type=(?P<type>\d)/$', views.register_test, name='register_test')
]