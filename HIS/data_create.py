import enum
import random
from string import ascii_letters
from datetime import datetime
from django.conf import settings
import os
import django
from django.contrib.auth.hashers import make_password
import pandas as pd
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HIS.settings")
django.setup()
from datetime import timedelta, datetime
from login.models import User
from appoint.models import Department, Doctor, Schedule, Order
from django.utils.timezone import now
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import string


def create_name_sex():
    # 删减部分 ，比较大众化姓氏
    firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻水云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅卞齐康伍余元卜顾孟平" \
                "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计成戴宋茅庞熊纪舒屈项祝董粱杜阮席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田胡凌霍万柯卢莫房缪干解应宗丁宣邓郁单杭洪包诸左石崔吉" \
                "龚程邢滑裴陆荣翁荀羊甄家封芮储靳邴松井富乌焦巴弓牧隗山谷车侯伊宁仇祖武符刘景詹束龙叶幸司韶黎乔苍双闻莘劳逄姬冉宰桂牛寿通边燕冀尚农温庄晏瞿茹习鱼容向古戈终居衡步都耿满弘国文东殴沃曾关红游盖益桓公晋楚闫"
    # 百家姓全部姓氏
    # firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平" \
    #             "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董粱杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮" \
    #             "龚程嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴欎胥能苍" \
    #             "双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍舄璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空" \
    #             "曾毋沙乜养鞠须丰巢关蒯相查後荆红游竺权逯盖益桓公晋楚闫法汝鄢涂钦归海帅缑亢况后有琴梁丘左丘商牟佘佴伯赏南宫墨哈谯笪年爱阳佟言福百家姓终"
    # 百家姓中双姓氏
    firstName2 = "万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁段干百里东郭南门呼延羊舌微生梁丘左丘东门西门南宫南宫"
    # 女孩名字
    girl = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽'
    # 男孩名字
    boy = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
    # 名
    name = '中笑贝凯歌易仁器义礼智信友上都卡被好无九加电金马钰玉忠孝'

    # 10%的机遇生成双数姓氏
    if random.choice(range(100)) > 10:
        firstName_name = firstName[random.choice(range(len(firstName)))]
    else:
        i = random.choice(range(len(firstName2)))
        firstName_name = firstName2[i:i + 2]

    sex = random.choice(range(2))
    name_1 = ""
    # 生成并返回一个名字
    if sex > 0:
        girl_name = girl[random.choice(range(len(girl)))]
        if random.choice(range(2)) > 0:
            name_1 = name[random.choice(range(len(name)))]
        return [firstName_name + name_1 + girl_name, 0]
    else:
        boy_name = boy[random.choice(range(len(boy)))]
        if random.choice(range(2)) > 0:
            name_1 = name[random.choice(range(len(name)))]
        return [firstName_name + name_1 + boy_name, 1]


def create_age():
    return random.randint(10, 90)


def create_phone():
    head = '1'
    for i in range(10):
        head += str(random.randint(0, 9))
    return head


def create_email():
    postfixes = ['163', 'outlook', 'qq', 'gamil', '126']
    postfix = '@' + postfixes[random.randint(0, len(postfixes)-1)]+'.com'
    email = ''
    for i in range(13):
        email += ascii_letters[random.randint(0, len(ascii_letters)-1)]
    email += postfix
    return email


def create_user():

    [name, sex] = create_name_sex()
    age = create_age()
    password = make_password(name, None)
    phone = create_phone()
    email = create_email()
    print(email)
    sign_up_time = now()
    appoint_times = 3
    appoint_available = 1
    birth = datetime.datetime.today() - timedelta(days=365*age)
    new_user = User.objects.create(name=name, sex=sex, age=age, password=password, phone=phone, birth=birth, email=email, sign_up_time=sign_up_time,
                                   appoint_times=appoint_times, appoint_available=appoint_available)
    new_user.save()


def create_location():
    locations = [
        '一楼',
        '二楼',
        '三楼',
        '四楼',
        '五楼'
    ]
    return locations[random.randint(0, len(locations)-1)]


def create_department(departments):
    check_departments = [
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
    # departments = [
    #     '牙科',
    #     '骨科',
    #     '儿科',
    #     '妇产科',
    #     '疼痛科',
    #     '中医科',
    #     '口腔科',
    #     '麻醉科',
    #     '体检科',
    #     '急诊科',
    #     '胸外科',
    #     '感染科',
    #     '血管外科',
    #     '消化内科',
    #     '血液内科',
    #     '肝胆外科',
    #     '泌尿外科',
    #     '普通外科',
    #     '神经内科',
    #     '神经外科',
    #     '乳腺外科',
    #     '新生儿科',
    #     '肿瘤内科',
    #     '肿瘤外科',
    #     '心血管内科',
    #     '心血管外科',
    #     '生殖医学科',
    #     '风湿免疫科',
    #     '康复医学科',
    #     '精神心理科',
    #     '重症医学科',
    #     '皮肤性病科',
    #     '老年内一科',
    #     '老年内二科',
    #     '肿瘤放疗科',
    #     '内分泌代谢科',
    #     '心脏病科呼吸与危重症医学科',
    #     '结构性耳鼻咽喉-头颈外科',
    #     '肾内科'
    # ]
    for department in departments:
        location = create_location()
        Department.objects.create(name=department, location=location, type=0)
    for check_department in check_departments:
        location = create_location()
        Department.objects.create(name=check_department, location=location, type=1)


def create_doctor(doctors, departments):
    titles = {
        # '主任医师': 1,
        # '副主任医师': 2,
        # '主治医师': 2,
        '住院医师': 3,
        '实习医师': 2
    }

    for index, doctor in enumerate(doctors):
        doctor = doctor[1]
        department_id = index % 16
        print(index)
        department_name = departments[department_id]
        print(department_name)
        department = Department.objects.get(name=department_name)
        name = doctor[1]
        sex = 0 if doctor[2] == '女' else 1
        title = doctor[4]
        strength = doctor[5] if index % 5 in [0, 1, 2] else ''
        Doctor.objects.create(name=name, sex=sex, title=title, strength=strength, department=department)

    for department in Department.objects.filter(type=1):
        for title in titles.keys():
            num = titles[title]
            for i in range(num):
                name, sex = create_name_sex()
                strength = ''
                Doctor.objects.create(name=name, sex=sex, title=title, strength=strength, department=department)


def create_schedule():
    work_day_nums = [3, 4, 5]
    for doctor in Doctor.objects.all():
        if doctor.title not in ['住院医师', '实习医师']:
            work_day_num = work_day_nums[random.randint(0, 2)]
            for week_day in random.sample(range(1, 8), work_day_num):
                num = 30
                price = 80
                for morning_afternoon in [0, 1]:
                    Schedule.objects.create(weekday=week_day, doctor=doctor, department=doctor.department,
                                            morning_afternoon=morning_afternoon, num=num, type=1, price=price)

    for department in Department.objects.all():
        print(department.name)
        work_day_num = work_day_nums[random.randint(0, 2)]
        for week_day in random.sample(range(1, 8), work_day_num):
            num = 100
            price = 50
            for morning_afternoon in [0, 1]:
                Schedule.objects.create(weekday=week_day, department=department,
                                        morning_afternoon=morning_afternoon, num=num, type=0, price=price)


if __name__ == '__main__':
    # for i in range(100):
    #     create_user()
    # create_schedule()
    # departments = pd.read_excel('/Users/tantianyi/PycharmProjects/HIS/data/医院挂号信息.xlsx', engine='openpyxl', sheet_name='科室信息')
    # doctors = pd.read_excel('/Users/tantianyi/PycharmProjects/HIS/data/医院挂号信息.xlsx', engine='openpyxl', sheet_name='医师信息')
    # # print(list(departments['名称']))
    # # print(list(doctors.iterrows()))
    # for row in doctors.iterrows():
    #     print('医师' in row[1][4])
    # Department.objects.get(name='妇产科')
    # departments = list(departments['名称'])
    # print(departments)
    # # create_department(list(departments['名称']))
    # Doctor.objects.all().delete()
    # create_doctor(doctors.iterrows(), departments)
    # Schedule.objects.all().delete()
    # create_schedule()
    # User.objects.create(name='谭天一', sex=1, age=21, password=make_password('谭天一', None), phone=13124766566, birth=datetime.today() - timedelta(days=365*21), email='antonio21tan@163.com',
    #                     sign_up_time=now(),
    #                     appoint_times=3, appoint_available=1, admin=1)
    # for schedule in Schedule.objects.filter(type=0, weekday=datetime.isoweekday(datetime.today().date())):
    #     print(schedule.department.name)
    #
    # print()
    # for department in Department.objects.all():
    #     print(department.name)
    # print(Schedule.objects.filter(department=Department.objects.get(id=int('95'))))
    # orders = Order.objects.filter(status=4)
    # print(orders[0].status)
    # # department = Department.objects.get(id=0)
    # # print(len(department))
    #
    #
    # sender = '2017312322@email.cufe.edu.cn'
    # receivers = ['antonio21tan@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #
    # # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    # msg = ""
    # code = ''
    # for i in range(4):
    #     code += string.ascii_letters[random.randint(0, 51)]
    # message = MIMEText('您的邮箱验证码是%s'%code, 'plain', 'utf-8')
    # message['From'] = Header("CUFE医院患者服务系统", 'utf-8')   # 发送者
    # message['To'] =  Header("用户", 'utf-8')        # 接收者
    #
    # subject = 'CUFE医院患者服务系统邮箱验证码'
    # message['Subject'] = Header(subject, 'utf-8')
    #
    #
    # try:
    #     smtpObj = smtplib.SMTP(host='smtp.exmail.qq.com', port=25)
    #     smtpObj.login(user=sender, password='r9FMXKRcmDXo5DNb')
    #     smtpObj.set_debuglevel(1)
    #     smtpObj.sendmail(sender, receivers, message.as_string())
    #     print("邮件发送成功")
    # except smtplib.SMTPException:
    #     print("Error: 无法发送邮件")
    # print(User.objects.get(id='100'))
    orders = Order.objects.filter(status=2, order_time=datetime.today())
    print(len(orders))