from datetime import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
class Subject(models.Model):
    sub_name = models.CharField(max_length=15)

class Admin(models.Model):
    a_name= models.CharField(max_length=30)
    a_email = models.CharField(max_length=40)
    a_contact = models.IntegerField()
    a_dob = models.DateField()
    a_gender = models.TextChoices('Gender','Male Female')
    a_password = models.CharField(max_length=15)

class Teacher(models.Model):
    t_name= models.CharField(max_length=30)
    t_email = models.CharField(max_length=40)
    t_contact = models.BigIntegerField()
    t_exp = models.IntegerField()
    t_password = models.CharField(max_length=15)
    t_regdate = models.DateTimeField(auto_now_add=True)
    t_sub = models.ForeignKey(Subject,on_delete=models.CASCADE)
    t_req = models.CharField(max_length=10)

class Student(models.Model):
    s_name= models.CharField(max_length=30)
    s_email = models.CharField(max_length=40)
    s_contact = models.BigIntegerField()
    s_class = models.CharField(max_length=30)
    s_add = models.TextField()
    s_password = models.CharField(max_length=15)
    s_regdate = models.DateTimeField(auto_now_add=True)
    s_req = models.CharField(max_length=10)

class temp(models.Model):
    temp = models.CharField(max_length=10)

class Feedback(models.Model):
    stu_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    f_date = models.DateTimeField()
    f_message = models.CharField(max_length=50)

class Attendance(models.Model):
    stu_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    att_date = models.DateTimeField()
    ispresent = models.BooleanField()

class Exam(models.Model):
    sub_id = models.ForeignKey(Subject,on_delete=models.CASCADE)
    ex_start = models.DateTimeField()
    ex_end = models.DateTimeField()
    ex_duration = models.IntegerField()
    ex_title = models.CharField(max_length=15)

class Question(models.Model):
    ex_id = models.ForeignKey(Exam,on_delete=models.CASCADE)
    que = models.CharField(max_length=100)
    ans = models.CharField(max_length=50)
    opA = models.CharField(max_length=50)
    opB = models.CharField(max_length=50)
    opC = models.CharField(max_length=50)
    opD = models.CharField(max_length=50)
    

class Answer(models.Model):
    ans = models.TextChoices('Answer','A B C D')
    que_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    s_ans = models.ForeignKey(Student,on_delete=models.CASCADE)

class Result(models.Model):
    exam_id = models.ForeignKey(Exam,on_delete=models.CASCADE)
    stu_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    marks = models.IntegerField()
    total_marks = models.IntegerField(default=0)

class Scan(models.Model):
    scan_img = models.ImageField(upload_to='scan_image/')
