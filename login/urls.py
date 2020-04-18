from django.contrib import admin
from django.urls import path, re_path
from . import views
from .views import SignUpView, SignInView

app_name='login'
urlpatterns= [
    # path('sign_up_test/', views.sign_up_test, name='sign_up_test'),
    path('sign_up_test/', SignUpView.as_view(), name='sign_up_test'),
    re_path(r'^sign_up_test/welcome=(?P<name>.+)/$', views.welcome_sign_up, name='welcome_user_test'),
    path('sign_in_test/', SignInView.as_view(), name='sign_in_test'),
    re_path(r'^sign_in_test/user=(?P<name>.+)/$', views.welcome_login, name='welcome_login')
]

