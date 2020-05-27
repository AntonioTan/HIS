from django.urls import path, re_path
from . import views
from .views import AppointView, deal_date

app_name = 'appoint'
urlpatterns = [
    # path('register_test/', AppointView.as_view(), name='register_test'),
    re_path(
        r'^register_test/(department=(?P<department>\w+)/)?(doctor_id=(?P<doctor_id>\d+)/)?(weekday=(?P<weekday>\d)/)?(type=(?P<type>\d)/)?$',
        AppointView.as_view(), name='register_test'),
    re_path(
        r'^search/(change_page=(?P<change_page>\w+)/)?(picked_department_id=(?P<picked_department_id>\d+)/)?(picked_doctor_id=(?P<picked_doctor_id>\d+)/)?(picked_date=(?P<picked_date>\d)/)?(picked_type=(?P<picked_type>\d)/)?(picked_page=(?P<picked_page>\d+)/)?(picked_morning_afternoon=(?P<picked_morning_afternoon>\d)/)?$',
        AppointView.as_view(), name='search'),
    re_path(
        r'^registration/picked_department_id=(?P<picked_department_id>\d+)/(picked_doctor_id=(?P<picked_doctor_id>\d+)/)?picked_date=(?P<picked_date>\d)/picked_type=(?P<picked_type>\d)/picked_morning_afternoon=(?P<picked_morning_afternoon>\d)/$',
        views.deal_registration, name='registration'
    ),
    path('registration_test/<int:arg1>/', views.deal_registration, name='registration_test'),
    path('admin_search/', views.admin_search, name='admin_search'),
    path('admin_register/<int:order_id>/', views.admin_register, name='admin_register')
]
