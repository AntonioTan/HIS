from django.urls import path, re_path
from . import views
from .views import AppointView


app_name = 'appoint'
urlpatterns = [
    # path('register_test/', AppointView.as_view(), name='register_test'),
    re_path(r'^register_test/(department=(?P<department>\w+)/)?(doctor_id=(?P<doctor_id>\d+)/)?(weekday=(?P<weekday>\d)/)?(type=(?P<type>\d)/)?$', AppointView.as_view(), name='register_test')
]
