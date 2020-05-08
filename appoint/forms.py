from django.forms import Form
from django import forms
from datetime import datetime, timedelta

def get_seven_days():
    days = []
    today = datetime.today()
    for i in range(7):
        day = today + timedelta(days=i)
        days.append(('id_day' + str(i), day.strftime("%m月%d日")))
    days.sort()
    return days


class DatePickForm(Form):
    days = get_seven_days()
    dates = forms.ChoiceField(
        label='Date',
        choices=days,
        widget=forms.RadioSelect)