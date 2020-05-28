from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from .models import User
import datetime
import string


def validate_user_name(value):
    existed_user_error = ValidationError(
                ('用户名已存在: %s' % value),
                params={'value': value},
                code='用户名重复')
    try:
        a = User.objects.get(name=value)
        raise existed_user_error
    except MultipleObjectsReturned:
        raise existed_user_error
    except ObjectDoesNotExist:
        pass


def validate_user_phone(value):
    if len(value) != 11:
        raise ValidationError('请输入正确的手机号',
                              params={'value': value},
                              code='手机号长度错误')


def validate_user_birth(value):
    if int(value.year) < 1900:
        raise ValidationError('请输入真正的生日',
                              params={'value': value},
                              code='出生年份过老')
    try:
        datetime.datetime.strptime(str(value), '%Y-%m-%d')
    except ValueError:
        raise ValidationError(("错误的日期格式 应该是 YYYY-MM-DD"), params=value, code="日期格式错误")


def validate_user_password(value):
    # TODO add this later we still need to test...
    nums = list(range(10))
    upper_letters = string.ascii_uppercase
    if(len(value)) == 0:
        raise (ValidationError('请输入密码',
                               params={'value': value},
                               code='请输入密码'))
    if(len(value)) < 8:
        raise(ValidationError('密码长度过短',
                              params={'value': value},
                              code='密码长度过短'))
    no_num = True
    for num in nums:
        if str(num) in value:
            no_num = False
    if no_num:
        raise(ValidationError('密码没有数字',
                              params={'value': value},
                              code='密码没有数字'))
    no_upper = True
    for upper_letter in upper_letters:
        if upper_letter in value:
            no_upper = False
    if no_upper:
        raise(ValidationError('密码没有大写字母',
                              params={'value':value},
                              code='密码没有大写字母'))




