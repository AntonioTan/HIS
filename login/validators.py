from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from .models import User


def validate_user_name(value):
    existed_user_error = ValidationError(
                ('User Name Already Exists: %(value)s'),
                params={'value': value},
                code='用户名重复')
    try:
        a = User.objects.get(name=value)
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


def validate_user_password(value):
    # TODO add this later we still need to test...
    return

