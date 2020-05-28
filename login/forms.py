from django import forms
from .validators import validate_user_name, validate_user_phone, validate_user_birth, validate_user_password
from . import choices


class SignIn(forms.Form):
    name = forms.CharField(max_length=20,
                           label='用户名',
                           error_messages={
                               'required': '请输入用户名'
                           }
                           )
    password = forms.CharField(max_length=20,
                               label='密码',
                               )


class SignUp(forms.Form):
    # basically this form is consistent with the User model
    # Alert -> if we change the User model, don't forget changing the form here
    name = forms.CharField(max_length=20,
                           label='用户名',
                           error_messages={
                               'required': '请输入用户名'
                           },
                           validators=[validate_user_name])

    password = forms.CharField(max_length=20,
                               label='密码',
                               error_messages={
                                   'required': '请输入密码'
                               },
                               validators=[validate_user_password]
                               )

    birth = forms.DateField(label="生日",
                            help_text='1999-09-03',
                            error_messages={
                                'required': '请输入生日'
                            },
                            validators=[validate_user_birth])

    sex = forms.ChoiceField(label="性别",
                            error_messages={
                                'required': '请选择性别'
                            },
                            choices=choices.SEX_CHOICES,
                            widget=forms.RadioSelect)

    phone = forms.CharField(max_length=11,
                            label='手机号',
                            error_messages={
                                'required': '请输入手机号'
                            },
                            validators=[validate_user_phone])

    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'required': '请输入邮箱'
                             }
                             )


class ChangePSW(forms.Form):
    password = forms.CharField(max_length=20,
                               label='密码',
                               error_messages={
                                   'required': '请输入密码'
                               },
                               validators=[validate_user_password]
                               )
    repeat_password = forms.CharField(max_length=20,
                               label='重复密码',
                               error_messages={
                                   'required': '请输入密码'
                               },
                               validators=[validate_user_password]
                               )