from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
from datetime import datetime, timedelta
from appoint.models import Order, Report
from login.models import User
import string, random
from email.mime.text import MIMEText
from email.header import Header
import smtplib


# Create your views here.
def change_info(request):
    print(request.COOKIES)
    if 'user_id' in request.COOKIES.keys():
        user_id = request.COOKIES['user_id']
        user = User.objects.get(id=user_id)
        if request.method != 'POST':
            return render(request, template_name='login/revise.html', context={'user_id':user.id, 'user_name': user.name, 'user_sex': user.sex})
        if user.admin:
            return render(request, template_name='login/home_page.html')
        user_data = {}
        user_data['name'] = 'TEST'
        user_data['password'] = 'test'
        user_data['sex'] = 'female'
        user_data['age'] = 18
        user_data['birth'] = request.POST['birth']
        user_data['email'] = request.POST['email']
        user_data['phone'] = request.POST['phone']
        form = SignUp(user_data)
        if form.is_valid():
            print(user_data)
            age = date.today().year - int(user_data['birth'][0:4])
            user.birth = user_data['birth']
            user.email = user_data['email']
            user.phone = user_data['phone']
            user.age = date.today().year - int(user_data['birth'][0:4])
            user.save()
            print('Saved')
            user = User.objects.get(id=user_id)
            context = get_user_center_context(user.name)
            context = add_user_id(request, context)
            context['user_name'] = user.name
            context['user_id'] = user.id
            context['user_sex'] = user.sex
            response = render(request, template_name='login/user_center.html', context=context)
        else:
            errors = form.errors.as_data()
            for error_key in errors.keys():
                errors[error_key] = errors[error_key][0].message
            print(errors)
            context = {'errors': errors}
            context = add_user_id(request, context)
            context['user_name'] = user.name
            context['user_id'] = user.id
            context['user_sex'] = user.sex
            response = render(request, template_name='login/revise.html', context=context)
        response.set_cookie(key='user_id', value=user_id, expires=3600)
        return response
    else:
        return render(request, template_name='login/home_page.html')


def change_psw(request):
    rst = {}
    for key in request.POST.keys():
        rst[key] = request.POST[key]
    print(rst)
    if len(rst['password']) == 0 or len(rst['new_password']) == 0:
        context = rst
        context['error'] = '请填写密码'
        return render(request, template_name='login/password_changed.html', context=context)
    if rst['password'] != rst['new_password']:
        context = rst
        context['error'] = '两次密码不一样'
        return render(request, template_name='login/password_changed.html', context=context)
    user = User.objects.get(id=rst['user_id'])
    user.password = make_password(rst['new_password'])
    user.save()
    return render(request, template_name='login/home_page.html')


def get_code(request, name, email):
    find_template = 'login/forget.html'
    sender = '2017312322@email.cufe.edu.cn'
    receivers = ['antonio21tan@163.com']
    code = ''
    for i in range(4):
        code += string.ascii_letters[random.randint(0, 51)]
    msg = ""
    message = MIMEText('您的邮箱验证码是%s' % code, 'plain', 'utf-8')
    message['From'] = Header("CUFE医院患者服务系统", 'utf-8')  # 发送者
    message['To'] = Header("用户", 'utf-8')  # 接收者
    subject = 'CUFE医院患者服务系统邮箱验证码'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP(host='smtp.exmail.qq.com', port=25)
        smtpObj.login(user=sender, password='r9FMXKRcmDXo5DNb')
        smtpObj.set_debuglevel(1)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    context = {
        'name': name,
        'email': email,
        'real_code': code
    }
    return render(request, template_name=find_template, context=context)


class FindView(View):
    initial = {
        'name': 'Eric',
        'email': '203i0908@163.com'
    }
    template_name = 'login/forget.html'
    success_template_name = 'login/password_changed.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request)
        else:
            if 'user_id' in request.COOKIES.keys():
                self.initial['user_id'] = request.COOKIES['user_id']
            else:
                self.initial['user_id'] = -1
            context = self.initial
            return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        context = {}
        for key in request.POST.keys():
            context[key] = request.POST[key]
        print(context)
        if context['name'] == '' or context['email'] == '':
            context = self.initial
            context['error'] = '请输入用户名和邮箱'
            return render(request, template_name=self.template_name, context=context)
        elif context['real_code'] == '':
            context['error'] = '请获取验证码'
            return render(request, template_name=self.template_name, context=context)
        elif context['code'] == '':
            context['error'] = '请输入验证码'
            return render(request, template_name=self.template_name, context=context)
        else:
            name = request.POST['name']
            email = request.POST['email']
            code = request.POST['code']
            try:
                user = User.objects.get(name=name, email=email)
                context['user_id'] = user.id
            except Exception:
                context['error'] = '用户名或邮箱错误'
                return render(request, template_name=self.template_name, context=context)
            if context['real_code'] == context['code']:
                return render(request, template_name=self.success_template_name, context=context)
            else:
                context['error'] = '验证码错误 请重新获取'
                return render(request, template_name=self.template_name, context=context)


def department_list(request):
    print(request.COOKIES)
    if 'user_id' in request.COOKIES.keys():
        context = {'user_id': request.COOKIES['user_id']}
    else:
        context = {}
    department_list_template = 'login/department.html'
    return render(request, template_name=department_list_template, context=context)


def our_help(request):
    if 'user_id' in request.COOKIES.keys():
        context = {'user_id': request.COOKIES['user_id']}
    else:
        context = {}
    help_template = 'login/help_center.html'
    return render(request, template_name= help_template, context=context)


def contact(request):
    print(request.COOKIES)
    if 'user_id' in request.COOKIES.keys():
        context = {'user_id': request.COOKIES['user_id']}
    else:
        context = {}
    contact_template = 'login/contact.html'
    return render(request, template_name=contact_template, context=context)


def user_center(request):
    print(request.COOKIES)
    if 'user_id' in request.COOKIES:
        user_id = request.COOKIES['user_id']
        name = User.objects.get(id=user_id).name
        context = get_user_center_context(name)
        context = add_user_id(request, context)
        response = render(request, template_name='login/user_center.html', context=context)
        response.set_cookie(key='user_id', value=user_id, expires=3600)
        return response
    else:
        return render(request, template_name='login/home_page.html')


def logout(request):
    context = {'sign_in_form': SignIn()}
    response = render(request, 'login/home_page.html', context=context)
    response.set_cookie(key='post_token', value='allow')
    response.delete_cookie('user_id')
    return response


def sign_up_test(request):
    sign_up_form = SignUp()
    context = {
        "sign_up_form": sign_up_form
    }
    context = add_user_id(request, context)
    return render(request, 'login/sign_up_test.html', context=context)


def welcome_sign_up(request, name):
    return render(request, 'login/welcome_user_test.html', context={'user_name': name})


def welcome_login(request, name):
    return render(request, 'login/welcome_login_test.html', context={'name': name})


class SignInView(View):
    form_class = SignIn
    initial = {'key': 'value'}
    template_name='login/home_page.html'
    admin_template_name = 'appoint/admin.html'
    success_template_name = 'login/user_center.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request)
        else:
            if 'post_token' not in request.COOKIES.keys():
                print('request', request.COOKIES)
                request.COOKIES['post_token'] = 'allow'
            if request.COOKIES['post_token'] != 'allow':
                return redirect('appoint:search')
            context = {'sign_in_form': SignIn()}
            context = add_user_id(request, context)
            response = render(request, self.template_name, context=context)
            response.set_cookie(key='post_token', value='allow')
            return response

    def get(self, request):
        print('get')

    def post(self, request):
        self.initial = request.POST
        print(self.initial)
        print('post', request.COOKIES)
        # TODO we need direct user to home_page_logged_in
        if 'post_token' not in request.COOKIES.keys() or request.COOKIES['post_token'] != 'allow':
            return redirect('appoint:search')
        if verify_sign_in(self.initial):
            context = get_user_center_context(self.initial['name'])
            print(context)
            if 'admin' in context.keys():
                response = render(request, self.admin_template_name, context=context)
                response.set_cookie(key='post_token', value='disable', expires=3600)
                response.set_cookie(key='user_id', value=context['user'].id, expires=3600)
                return response
            else:
                context = add_user_id(request, context)
                response = render(request, self.success_template_name, context=context)
                response.set_cookie(key='post_token', value='disable', expires=3600)
                response.set_cookie(key='user_id', value=context['user'].id, expires=3600)
                return response
        else:
            # form = self.form_class(self.initial)
            # TODO we need to show user what's wrong with his account or password
            context = {'error': '用户名或密码错误'}
            context = add_user_id(request, context)
            return render(request, template_name=self.template_name, context=context)


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
    success_template_name = "login/signup_success.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request)
        else:
            form = SignUp()
            context = {'sign_up_form': form}
            context = add_user_id(request, context)
            response = render(request, 'login/sign_up.html', context)
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
        if 'post_token' not in request.COOKIES.keys() or request.COOKIES['post_token'] != 'allow':
            return redirect('appoint:search')
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
                # TODO add cleaned_data
            cleaned_data = form.cleaned_data
            context = {'sign_up_form': form, 'errors': errors}
            context = add_user_id(request, context)
            return render(request, template_name=self.template_name, context=context)


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
    print(sign_in_user)
    if sign_in_user.admin:
        return {
            'user': sign_in_user,
            'admin': 1
        }
    else:
        # get all registrations
        all_orders = Order.objects.filter(patient=sign_in_user)
        # get today registrations
        today_date = datetime.today().date()
        today_start_datetime = today_date
        today_end_datetime = today_start_datetime + timedelta(days=7)
        today_orders = all_orders.filter(order_time__range=(today_start_datetime, today_end_datetime))
        against_rule_orders = all_orders.filter(status=4)
        history_orders = all_orders.exclude(order_time__range=(today_start_datetime, today_end_datetime))
        reports = Report.objects.filter(patient=sign_in_user)
        context = {
            'user': sign_in_user,
            'today_orders': today_orders,
            'history_orders': history_orders,
            'today_date': today_date,
            'against_rule_orders': against_rule_orders,
            'reports': reports,
        }
        return context


def add_user_id(request, context):
    if 'user_id' not in request.COOKIES.keys():
        context['user_id'] = -1
        context['user_available'] = -1
        return context
    else:
        context['user_id'] = request.COOKIES['user_id']
        context['user_available'] = User.objects.get(id=request.COOKIES['user_id']).appoint_available
        return context

