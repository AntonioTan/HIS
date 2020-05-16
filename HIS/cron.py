from appoint import models


def test():
    print('cronb test!')


def test1():
    new_doctor = models.Doctor.objects.create(name='test',
                                 sex=1,
                                 title='test',
                                 strength='test',
                                 department=models.Department.objects.all()[0],)
    new_doctor.save()

