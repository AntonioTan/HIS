from django import forms
from .validators import validate_user_name, validate_user_phone, validate_user_birth
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
                               )

    birth = forms.DateField(label="生日",
                            help_text='1999-09-03',
                            validators=[validate_user_birth])

    sex = forms.ChoiceField(label="性别",
                            choices=choices.SEX_CHOICES,
                            widget=forms.RadioSelect)

    phone = forms.CharField(max_length=11,
                            label='手机号',
                            validators=[validate_user_phone])

    email = forms.EmailField(label='邮箱')

