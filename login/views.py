from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
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
    success_template_name='login/user_center_test.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request)
        else:
            if request.COOKIES['post_token'] != 'allow':
                return render(request, 'home_page_login_test.html')
            form = SignIn()
            response = render(request, 'login/home_page_test.html', context={'sign_in_form': form})
            response.set_cookie(key='post_token', value='allow')
            return response

    def get(self, request):
        return

    def post(self, request):
        self.initial = request.POST
        print(self.initial)
        if request.COOKIES['post_token'] != 'allow':
            return render(request, '.html')
        if verify_sign_in(self.initial):
            # get user
            sign_in_user = User.objects.get(name=self.initial['name'])
            # get today registrations
            today_orders = Order.objects.filter(status=2, patient=sign_in_user)
            today_registrations = [today_order.registration for today_order in today_orders]
            # get all registrations
            all_orders = Order.objects.filter(patient=sign_in_user)
            all_registrations = [order.registration for order in all_orders]
            context = {
                'user': sign_in_user,
                'today_regestrations': today_registrations,
                'all_registrations': all_registrations
            }
            response = render(request=request, template_name=self.success_template_name, context={'user': sign_in_user})
            response.set_cookie(key='post_token', value='disable')
            response.set_cookie(key='user_id', value=sign_in_user.id)
            return response
        else:
            form = self.form_class(self.initial)
            return render(request, template_name=self.template_name, context={'sign_in_form': form})


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
    template_name = "login/sign_up_test.html"
    success_template_name = "login/welcome_user_test.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request)
        else:
            form = SignUp()
            response = render(request, 'login/sign_up_test.html', context={'sign_up_form': form})
            response.set_cookie(key='post_token', value='allow')
            return response

    def get(self, request, *args, **kwargs):
        # we don't need this yet
        return

    def post(self, request, *args, **kwargs):
        self.initial = request.POST
        form = self.form_class(self.initial)
        if request.COOKIES['post_token'] != 'allow':
            return render(request, 'home_page_login_test.html')
        if form.is_valid():
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
            response = HttpResponseRedirect('welcome=%s' % user_data['name'])
            response.set_cookie(key='post_token', value='disable')
            return response
        else:
            return render(request, template_name=self.template_name, context={'sign_up_form': form})


def get_user_data(form_data):
    user_data = {}
    user_data['name'] = form_data['name']
    # Look OUT I use make_password here!
    user_data['password'] = make_password(form_data['password'], None)
    user_data['sex'] = True if form_data['sex']=='male' else False
    user_data['phone'] = form_data['phone']
    user_data['birth'] = form_data['birth']
    user_data['email'] = form_data['email']
    user_data['age'] = date.today().year - int(user_data['birth'][0:4])
    user_data['sign_up_time'] = datetime.now()
    # TODO we need to change the appoint time here later
    user_data['appoint_times'] = 3
    user_data['appoint_available'] = True
    return user_data
