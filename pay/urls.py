from django.urls import path, re_path
from .views import pay_test, pay_result

app_name='pay'
urlpatterns=[
    path('pay_test/<int:arg1>/', pay_test, name='pay_test'),
    path('pay_result/', pay_result, name='pay_result'),
]