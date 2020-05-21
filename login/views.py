from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.http.cookie import SimpleCookie
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HIS.settings")  # project_name 项目名称
django.setup()
from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from .forms import SignUp, SignIn
from .models import User
from datetime import date
from datetime import datetime
from appoint.models import Order
# Create your views here.


def user_center(request, name):
    context = get_user_center_context(name)
    return render(request, template_name='login/user_center_test.html', context=context)


def logout(request):
    response = render(request, 'login/home_page_test.html', context={'sign_in_form': SignIn()})
    response.set_cookie(key='post_token', value='allow')
    response.delete_cookie('user_id')
    return response


def sign_up_test(request):
    sign_up_form = SignUp()
    context = {
        "sign_up_form": sign_up_form
    }
    return render(request, 'login/sign_up_test.html', context=context)


def welcome_sign_up(request, name):
    return render(request, 'login/welcome_user_test.html', context={'user_name': name})


def welcome_login(request, name):
    return render(request, 'login/welcome_login_test.html', context={'name': name})


class SignInView(View):
    form_class = SignIn
    initial = {'key': 'value'}
    template_name='login/home_page_test.html'
    success_template_name = 'login/user_center_test.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request)
        else:
            if request.COOKIES['post_token'] != 'allow':
                return redirect('appoint:search_test')
            response = render(request, self.template_name, context={'sign_in_form': SignIn()})
            response.set_cookie(key='post_token', value='allow')
            return response

    def get(self, request):
        return

    def post(self, request):
        print(request.COOKIES)
        self.initial = request.POST
        print(self.initial)
        print(request.COOKIES)
        # TODO we need direct user to home_page_logged_in
        if request.COOKIES['post_token'] != 'allow':
            return redirect('appoint:search_test')
        if verify_sign_in(self.initial):
            context = get_user_center_context(self.initial['name'])
            response = render(request, self.success_template_name, context=context)
            response.set_cookie(key='post_token', value='disable', expires=3600)
            response.set_cookie(key='user_id', value=context['user'].id, expires=3600)
            print('Response')
            return response
        else:
            # form = self.form_class(self.initial)
            # TODO we need to show user what's wrong with his account or password
            return render(request, template_name=self.template_name, context={'error': '用户名或密码错误'})


def verify_sign_in(sign_in_data):
    name = sign_in_data['name']
    password = sign_in_data['password']
    try:
        encoded_password = User.objects.get(name=name).password
        check = check_password(password=password, encoded=encoded_password)
    except ObjectDoesNotExist:
        return False
    return check


class SignUpView(View):
    form_class = SignUp
    initial = {"key": "value"}
    # TODO here we use the test html later we need to change it
    template_name = "login/sign_up.html"
    success_template_name = "login/sign_up_success_test.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request)
        else:
            form = SignUp()
            response = render(request, 'login/sign_up.html', context={'sign_up_form': form})
            response.set_cookie(key='post_token', value='allow', expires=3600)
            return response

    def get(self, request, *args, **kwargs):
        # we don't need this yet
        return

    def post(self, request, *args, **kwargs):
        self.initial = request.POST
        print(self.initial)
        form = self.form_class(
            self.initial
        )
        if request.COOKIES['post_token'] != 'allow':
            return redirect('appoint:search_test')
        if self.initial['password'] == self.initial['repeat_password'] and form.is_valid():
            print('No Wrong')
            user_data = get_user_data(self.initial)
            new_user = User.objects.create(
                name=user_data['name'],
                password=user_data['password'],
                birth=user_data['birth'],
                age=user_data['age'],
                sex=user_data['sex'],
                phone=user_data['phone'],
                email=user_data['email'],
                sign_up_time=user_data['sign_up_time'],
                appoint_times=user_data['appoint_times'],
                appoint_available=user_data['appoint_available']
            )
            new_user.save()
            # response = HttpResponseRedirect('welcome=%s' % user_data['name'])
            response = render(request, self.success_template_name)
            response.set_cookie(key='post_token', value='disable', expires=3600)
            return response
        else:
            errors = form.errors.as_data()
            for error_key in errors.keys():
                errors[error_key] = errors[error_key][0].message
            if self.initial['password'] != self.initial['repeat_password']:
                errors['repeat_password'] = '确认密码与密码不相同'
            cleaned_data = form.cleaned_data
            return render(request, template_name=self.template_name, context={'sign_up_form': form, 'errors': errors})


def get_user_data(form_data):
    user_data = {}
    user_data['name'] = form_data['name']
    # Look OUT I use make_password here!
    user_data['password'] = make_password(form_data['password'], None)
    user_data['sex'] = True if form_data['sex'] == 'male' else False
    user_data['phone'] = form_data['phone']
    user_data['birth'] = form_data['birth']
    user_data['email'] = form_data['email']
    user_data['age'] = date.today().year - int(user_data['birth'][0:4])
    user_data['sign_up_time'] = datetime.now()
    # TODO we need to change the appoint time here later
    user_data['appoint_times'] = 3
    user_data['appoint_available'] = True
    return user_data


def get_user_center_context(user_name):
    # get user
    sign_in_user = User.objects.get(name=user_name)
    # get all registrations
    all_orders = Order.objects.filter(patient=sign_in_user)
    # get today registrations
    today_date = datetime.today().date()
    today_start_datetime = datetime(year=today_date.year, month=today_date.month, day=today_date.day)
    today_end_datetime = datetime(year=today_date.year, month=today_date.month, day=today_date.day + 1)
    today_orders = all_orders.filter(order_time__range=(today_start_datetime, today_end_datetime))
    against_rule_orders = all_orders.filter(status=4)
    history_orders = []
    for order in all_orders:
        if order not in today_orders:
            history_orders.append(order)
    context = {
        'user': sign_in_user,
        'today_orders': today_orders,
        'history_orders': history_orders,
        'today_date': today_date,
        'against_rule_orders': against_rule_orders
    }
    return context