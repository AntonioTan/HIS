from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from .models import User
import datetime

def validate_user_name(value):
    existed_user_error = ValidationError(
                ('用户名已存在: %s'%value),
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
        raise ValidationError('Please enter valid phone number',
                              params={'value': value},
                              code='手机号长度错误')


def validate_user_birth(value):
    if int(value.year) < 1900:
        raise ValidationError('Please enter valid birth',
                              params={'value': value},
                              code='出生年份过老')
    try:
        datetime.datetime.strptime(str(value), '%Y-%m-%d')
    except ValueError:
        raise ValidationError(("错误的日期格式 应该是 YYYY-MM-DD"), params=value, code="日期格式错误")


def validate_user_password(value):
    # TODO add this later we still need to test...
    return



