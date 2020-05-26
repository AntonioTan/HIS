from django.contrib import admin
from django.urls import path, re_path
from . import views
from .views import SignUpView, SignInView, logout

app_name='login'
urlpatterns= [
    # path('sign_up_test/', views.sign_up_test, name='sign_up_test'),
    path('sign_up_test/', SignUpView.as_view(), name='sign_up_test'),
    re_path(r'^sign_up_test/welcome=(?P<name>.+)/$', views.welcome_sign_up, name='welcome_user_test'),
    path('sign_in/', SignInView.as_view(), name='sign_in'),
    re_path(r'^sign_in_test/user=(?P<name>.+)/$', views.welcome_login, name='welcome_login'),
    path('logout/', views.logout, name='logout'),
    path('user_center/', views.user_center, name='user_center'),
    path('contact/', views.contact, name='contact'),
    path('help/', views.help, name='help'),
    path('department_list/', views.department_list, name='department_list')
]

