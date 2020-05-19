from datetime import datetime, timedelta
from .models import Department, Doctor, Schedule
from math import ceil
weekdays = {
    1: '星期一',
    2: '星期二',
    3: '星期三',
    4: '星期四',
    5: '星期五',
    6: '星期六',
    7: '星期日'

}
department_names = [
        '儿科', '妇产科', '普外科', '泌尿外科', '神经外科', '心胸肿瘤外科', '骨科', '内科', '消化内科', '心内科', '呼吸内科', '眼科', '耳鼻喉科',
        '口腔科', '皮肤性病科', '中医科']
check_department_names = [
        '眼库',
        '病理科',
        '输血科',
        '药学部',
        '检验科',
        '营养科',
        '核医学科',
        '消毒供应科',
        '血液净化科',
        '医学影像科',
        '超声影像科'
    ]
types = ['普通号', '专家号']
morning_afternoons = ['上午', '下午']
appoint_basic_data = {
    'departments': [{'id': Department.objects.get(name=name).id, 'name': name} for name in department_names],
    'check_departments': [{'id': Department.objects.get(name=name).id, 'name': name} for name in check_department_names],
    'types': [{'id': types.index(name), 'name': name} for name in types],
    'dates': [{'text': str(datetime.today().date()+timedelta(days=i-1)) + weekdays[datetime.isoweekday(datetime.today().date()+timedelta(days=i-1))], 'id':i} for i in range(1, 8)],
    'tests': {'id': 0},
    'doctors': [{'id': doctor.id, 'name': doctor.name, 'sex': '男' if doctor.sex == 1 else '女',
                 'department_name': doctor.department.name, 'department_id': doctor.department.id, 'title': doctor.title} for doctor in Doctor.objects.filter(title='主任医师')],
    'schedules': [{'department_name': schedule.department.name, 'id': schedule.id} for schedule in Schedule.objects.filter(type=1, weekday=datetime.isoweekday(datetime.today().date()), morning_afternoon=0)],
    'schedule_objs': Schedule.objects.filter(type=1, weekday=datetime.isoweekday(datetime.today().date()), morning_afternoon=0),
    'doctor_objs': Doctor.objects.all(),
    'pages': list(range(1, ceil(len(Doctor.objects.filter(title='主任医师'))/8)+1)),
    'morning_afternoons': [{'id': morning_afternoons.index(morning_afternoon), 'name': morning_afternoon} for morning_afternoon in morning_afternoons],
    'picked_type': 1,
    'picked_page': 1,
    'picked_date': 0,
    'picked_morning_afternoon': 0,
    'page_schedules': [],
}
appoint_basic_data['page_doctors'] = appoint_basic_data['doctors'][0: 8]
