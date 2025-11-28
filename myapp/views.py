from datetime import date, datetime
from itertools import count
from urllib.request import Request
import numpy as np
from operator import attrgetter, eq
from django.shortcuts import redirect, render
from django.db.models.functions import (ExtractHour,ExtractMinute,ExtractSecond)
from django.utils import timezone
from .models import *

# Create your views here.

def index(request):
    return render(request,'index.html')

def login(request):
    print(request.POST)
    name = request.POST.get('login_id')
    passw = request.POST.get('login_pass') 
    cnt = 0
    tcnt = 0
    acnt = 0
    msg = ''
    try:
        student = Student.objects.filter(s_email=name)
        teach = Teacher.objects.filter(t_email=name)
        adm = Admin.objects.filter(a_email=name)
        for s in student:
            if s.s_password == passw:
                if s.s_req == 'None':
                    msg = 'Your application hasn\'t accepted yet.'
                    return render(request,'login.html',{'msg':msg})
                if s.s_req == 'Reject':
                    msg = 'Your application has Rejected.'
                    return render(request,'login.html',{'msg':msg})
                print('Student found')
                request.session['s_log']=s.id
                cnt += 1
                return redirect('../user/panel') 
        if cnt<1:
            print('Student NOt found')
        
        for t in teach:
            if t.t_password == passw:
                if t.t_req == 'None':
                    msg = 'Your application hasn\'t accepted yet.'
                    return render(request,'login.html',{'msg':msg})
                if t.t_req == 'Reject':
                    msg = 'Your application has Rejected.'
                    return render(request,'login.html',{'msg':msg})
                print('Teacher found')
                cnt += 1
                tcnt +=1
                return redirect('../teacher/panel')
        if cnt<1:
            print('Teacher NOt found')
        
        for a in adm:
            if a.a_password == passw:
                print('Admin found')
                request.session['a_log']=a.id
                # print(request.session['a_id'])
                # print(a.id)
                cnt += 1
                acnt += 1
                return redirect('../admin/panel')
        if cnt<1:
            print('Admin NOt found')
            msg = 'User Doesn\'t exists'

    except:
        print('Student NOt found')
        pass
    return render(request,'login.html',{'msg':msg})


def register(request):
    print(request.POST)
    msg = ''
    if(request.method=='POST'):
        stu = Student()
        teach = Teacher() 
        subj = Subject()
        cnt = 0
        data_name = request.POST.get('name')
        data_email = request.POST.get('email')
        eml = Student.objects.filter(s_email=data_email)
        for e in eml:
            cnt += 1
        eml = Admin.objects.filter(a_email=data_email)
        for e in eml:
            cnt += 1
        eml = Teacher.objects.filter(t_email=data_email)
        for e in eml:
            cnt += 1 
        if cnt>1:
            msg = 'User already exists, Please use different email.'
            return render(request,'register.html',{'msg':msg})
        data_pass= request.POST.get('pass')
        data_type = request.POST.get('type')
        data_add = request.POST.get('s_add')
        data_exp = request.POST.get('t_exp')
        data_req = 'None'
        
        if(request.POST.get('class')=='1'):
            data_class = 9
        elif(request.POST.get('class')=='2'):
            data_class = 10
        elif(request.POST.get('class')=='3'):
            data_class = 11
        elif(request.POST.get('class')=='4'):
            data_class = 12
        else:
            data_class = ''

        if(request.POST.get('t_sub')=='1'):
            data_sub = 'science'
        elif(request.POST.get('t_sub')=='2'):
            data_sub = 'maths'
        elif(request.POST.get('t_sub')=='3'):
            data_sub = 'social science'
        elif(request.POST.get('t_sub')=='4'):
            data_sub = 'english'
        else:
            data_sub = '' 
        data_phone = request.POST.get('phone')

        if(data_type == '1'):
            stu.s_name = data_name
            stu.s_email = data_email
            stu.s_password = data_pass
            stu.s_class = data_class
            print(data_add)
            stu.s_add = data_add
            stu.s_contact = data_phone
            stu.s_req = data_req
            stu.save()
            msg = 'Registration Succesful.'
        elif(data_type == '2'):
            eml = Teacher.objects.filter(t_email=data_email)
            teach.t_name = data_name
            teach.t_password = data_pass
            teach.t_email = data_email
            teach.t_contact = data_phone
            teach.t_exp = data_exp
            sub = Subject.objects.filter(sub_name=data_sub)
            cnt = 0
            for s in sub:
                cnt += 1
                teach.t_sub = s
            if cnt<1:   
                subj.sub_name = data_sub
                teach.t_sub = subj
                subj.save()
            teach.t_req = data_req
            teach.save() 
            msg = 'Registration Succesful.'
    return render(request,'register.html',{'msg':msg})
    
def contact(request):
    return render(request,'contact.html')

def calendar(request):
    return render(request,'view-attendance.html')


def userupcomingexam(request):
    # try:
    stu = Student.objects.filter(id=(request.session['s_log']))
    for s in stu:
        if request.session['s_log'] ==  s.id:
            print(request.session['s_log'])
            e = Exam.objects.filter(ex_end__gte = datetime.now())
            
            if('attend' in request.POST):
                id1 = request.POST.get('id')
                i = Exam.objects.get(id=id1)
                if(datetime.now()>=i.ex_start and datetime.now()<i.ex_end):
                    request.session['e_id'] = id1
                    return redirect('../user/attend-exam')
                
            prams ={
                'exams' : e
            }
            return render(request,'user-upcoming-exam.html',prams)
                # print(request.session['a_id'])
    # except:
    #     pass
    return redirect('../login')
    
def userattendexam(request):
    # try:
    s = Student.objects.get(id=(request.session['s_log']))
    
    if request.session['s_log'] ==  s.id:
        # print(request.session['s_log'])
        e = Exam.objects.get(id=request.session['e_id'])
        q = Question.objects.filter(ex_id=e)
        if request.method == 'POST':
            mark = 0
            tot = 0
            print(request.POST)
            for i in range(1,11):
                if(request.POST.get('op'+str(i))!=''and request.POST.get('qid'+str(i)) != None):
                    tot += 1
                    ans = request.POST.get('op'+str(i))
                    # print(ans+str(i))
                    # print('qid'+str(i))
                    # print(request.POST.get('qid'+str(i)))
                    qid = int(request.POST.get('qid'+str(i)))
                    ob = Question.objects.get(id=qid)
                    if ans == ob.ans:
                        mark += 1
            print(mark)
            rs = Result()
            rs.marks = mark
            rs.exam_id = e
            rs.stu_id = s
            rs.total_marks = tot
            rs.save()
            del request.session['e_id']
            return redirect('../user/upcoming-exam')
        
        # print(e.id)
        prams={
            'exams':e,
            'que':q,
        }
        return render(request,'user-attend-exam.html',prams)
                # print(request.session['a_id'])
    # except:
    #     pass
    return redirect('../login')
    
    
def userattendancereport(request):
    try:
        stu = Student.objects.filter(id=(request.session['s_log']))
        for s in stu:
            if request.session['s_log'] ==  s.id:
                print(request.session['s_log'])
                return render(request,'user-attendance-report.html')
                # print(request.session['a_id'])
    except:
        pass
    return redirect('../login')
    
def userexamreport(request):
    try:
        stu = Student.objects.filter(id=(request.session['s_log']))
        for s in stu:
            if request.session['s_log'] ==  s.id:
                print(request.session['s_log'])
                return render(request,'user-exam-report.html')
    except:
        pass
    return redirect('../login')
    
def userscanattendance(request):
    print(request.POST.get('result'))
    rst = {
        
    }
    return render(request,'user-scan-attendance.html',{'rst':rst})

def adminpanel(request):
    # return render(request,'admin-panel.html')
    try:
        adm = Admin.objects.filter(id=(request.session['a_log']))
        for a in adm:
            if request.session['a_log'] ==  a.id:
                print(request.session['a_log'])
                return render(request,'admin-panel.html')
                # print(request.session['a_id'])
    except:
        pass
    # return redirect('../login')
    return render(request,'admin-panel.html')

def adminsignuprequest(request):
    try:
        adm = Admin.objects.filter(id=(request.session['a_log']))
        for a in adm:
            if request.session['a_log'] ==  a.id:
                print(request.session['a_log'])
                teach = Teacher.objects.filter(t_req='None')
                print(request.POST)
                if(request.method=='POST' and 'accept' in request.POST):
                    print('accepted')
                    itm_id = request.POST.get('item_id')  
                    itm = Teacher.objects.get(id=int(itm_id))
                    itm.t_req = 'Accept'
                    print(itm.t_req)
                    itm.save()
                if(request.method=='POST' and 'reject' in request.POST):
                    print('rejected')
                    itm_id = request.POST.get('item_id')  
                    itm = Teacher.objects.get(id=int(itm_id))
                    itm.t_req = 'Reject'
                    print(itm.t_req)
                    itm.save()
                return render(request,'admin-signup-request.html',{'teach':teach})
                # print(request.session['a_id'])
    except:
        pass
    return redirect('../login')
    
def adminstudenttable(request):
    try:
        adm = Admin.objects.filter(id=(request.session['a_log']))
        for a in adm:
            if request.session['a_log'] ==  a.id:
                print(request.session['a_log'])
                stu = Student.objects.all()
                # for i in stu:
                    # print(i.id)
                if('search' in request.POST):
                    stu = Student.objects.filter(s_name=request.POST.get('data'))
                return render(request,'admin-student-table.html',{'stu':stu})
    except:
        pass
    return redirect('../login')

def adminteachertable(request):
    try:
        adm = Admin.objects.filter(id=(request.session['a_log']))
        for a in adm:
            if request.session['a_log'] ==  a.id:
                print(request.session['a_log'])
                tea = Teacher.objects.all()
                # for i in tea:
                    # print(i.id)
                print('Hello')
                if('search' in request.POST):
                    tea = Teacher.objects.filter(t_name=request.POST.get('data'))
                return render(request,'admin-teacher-table.html',{'tea':tea})
    except:
        pass
    return redirect('../login')

    
def userpanel(request):
    return render(request,'user-panel.html')

def teacherpanel(request):
    return render(request,'teacher-panel.html')


def teacherattendancereport(request):
    return render(request,'teacher-attendance-report.html')

def teacherexamreport(request):
    return render(request,'teacher-exam-report.html')

def teacherviewattendance(request):
    stu = Student.objects.all()
        # for i in stu:            # print(i.id)
    if('search' in request.POST):
        stu = Student.objects.filter(s_name__contains=request.POST.get('data'))
    return render(request,'teacher-view-attendance.html',{'stu':stu})

def teacherviewresult(request):
    stu = Student.objects.all()
        # for i in stu:            # print(i.id)
    if('search' in request.POST):
        stu = Student.objects.filter(s_name__contains=request.POST.get('data'))
    return render(request,'teacher-view-result.html',{'stu':stu})
    
def teachermarkattendance(request):
    if(request.method=='POST' and 'present' in request.POST):
        print('accepted')
        itm_id = request.POST.get('item_id')  
        itm = Student.objects.get(id=int(itm_id))
        attend = Attendance()
        attend.stu_id = itm
        attend.att_date = timezone.now()
        attend.ispresent = True
        attend.save()
    if(request.method=='POST' and 'absent' in request.POST):
        print('rejected')
        itm_id = request.POST.get('item_id')  
        itm = Student.objects.get(id=int(itm_id))
        attend = Attendance()
        attend.att_date = timezone.now()
        attend.stu_id = itm
        attend.ispresent = False
        attend.save()
    att = Attendance.objects.filter(att_date__contains = date.today())
    stuid = []
    for a in att:
        # print(a.stu_id.id)
        stuid.append(a.stu_id.id)
    print(stuid)
    stu = Student.objects.exclude(id__in = stuid)
        # for i in stu:            # print(i.id)
    if('search' in request.POST):
        stu = Student.objects.filter(s_name__contains=request.POST.get('data'))
    return render(request,'teacher-mark-attendance.html',{'stu':stu})
    
def teachersignuprequest(request):
    stu = Student.objects.filter(s_req='None')
    print(request.POST)
    if(request.method=='POST' and 'accept' in request.POST):
        print('accepted')
        itm_id = request.POST.get('item_id')  
        itm = Student.objects.get(id=int(itm_id))
        itm.s_req = 'Accept'
        print(itm.s_req)
        itm.save()
    if(request.method=='POST' and 'reject' in request.POST):
        print('rejected')
        itm_id = request.POST.get('item_id')  
        itm = Student.objects.get(id=int(itm_id))
        itm.s_req = 'Reject'
        print(itm.s_req)
        itm.save()
               
    return render(request,'teacher-signup-request.html',{'stu':stu})
    
def teacherstudenttable(request):
    stu = Student.objects.all()
        # for i in stu:            # print(i.id)
    if('search' in request.POST):
        stu = Student.objects.filter(s_name__contains=request.POST.get('data'))
    return render(request,'teacher-student-table.html',{'stu':stu})

def teacherupcomingexam(request):
    e = Exam.objects.filter(ex_end__gte = datetime.now())
    if('create' in request.POST):
        return redirect('../teacher/create-paper')
    if('edit' in request.POST):
        qid = request.POST.get('id')
        print("edit "+str(qid))
        request.session['q_id'] = qid
        print(request.session['q_id'])
        return redirect('../teacher/edit-paper')
    prams ={
        'exams' : e
    }
    return render(request,'teacher-upcoming-exam.html',prams)

def teachereditpaper(request):
    # try:
    # cnt = 1
    ex = Exam.objects.get(id=request.session['q_id'])
    print(ex.ex_title)
    qu = Question.objects.filter(ex_id = ex)
    print(request.session['q_id'])
    for q in qu:
        print(q.que)
        # l1 = []
        # l2 = []
        # for q in qu:
            # l1.append(cnt)
            # l2.append(q)
            # cnt += 1
    params= {
        'e' : ex,
        'list':qu,
    }
    if(request.method=='POST'):
        print(request.POST)
        data_sub = request.POST.get('subj')
        data_title = request.POST.get('title')
        data_start = request.POST.get('start')
        data_end = request.POST.get('end')
        data_que = []
        data_ans = []
        data_opA = []
        data_opB = []
        data_opC = []
        data_opD = []
        sid = Subject.objects.get(sub_name=data_sub)
        exam = Exam()
        exam.sub_id = sid
        exam.ex_start = data_start
        exam.ex_end = data_end
        start_dt = datetime.strptime(data_start, '%Y-%m-%dT%H:%M')
        end_dt = datetime.strptime(data_end, '%Y-%m-%dT%H:%M')
        diff = (end_dt - start_dt)    
        exam.ex_title = data_title
        exam.ex_duration = diff.seconds
        exam.save()
                
        for i in range(1,11):
            if request.POST.get('question'+str(i)) != '':
                data_que.append(request.POST.get('question'+str(i)))
                data_ans.append(request.POST.get('opt'+str(i)))
                data_opA.append(request.POST.get('optA'+str(i)))
                data_opB.append(request.POST.get('optB'+str(i)))
                data_opC.append(request.POST.get('optC'+str(i)))
                data_opD.append(request.POST.get('optD'+str(i)))
            
        for i in range(0,len(data_que)):
            q = Question()
            q.que = data_que[i]
            q.ans = data_ans[i]
            q.opA = data_opA[i]
            q.opB = data_opB[i]
            q.opC = data_opC[i]
            q.opD = data_opD[i]
            q.ex_id = exam
            q.save()
                            

        print("Q = "+str(data_que))
    return render(request,'teacher-edit-paper.html',params)
    # except:
    #     pass
    # return redirect('../teacher/upcoming-exam')

def teachercreatepaper(request):
    params= {
        'count':[1,2,3,4,5,6,7,8,9,10]
    }

    if(request.method=='POST'):
        print(request.POST)
        data_sub = request.POST.get('subj')
        data_title = request.POST.get('title')
        data_start = request.POST.get('start')
        data_end = request.POST.get('end')
        data_que = []
        data_ans = []
        data_opA = []
        data_opB = []
        data_opC = []
        data_opD = []
        sid = Subject.objects.get(sub_name=data_sub)
        exam = Exam()
        exam.sub_id = sid
        exam.ex_start = data_start
        exam.ex_end = data_end
        start_dt = datetime.strptime(data_start, '%Y-%m-%dT%H:%M')
        end_dt = datetime.strptime(data_end, '%Y-%m-%dT%H:%M')
        diff = (end_dt - start_dt)    
        exam.ex_title = data_title
        exam.ex_duration = diff.seconds
        exam.save()
               
        for i in range(1,11):
            if request.POST.get('question'+str(i)) != '':
                data_que.append(request.POST.get('question'+str(i)))
                data_ans.append(request.POST.get('opt'+str(i)))
                data_opA.append(request.POST.get('optA'+str(i)))
                data_opB.append(request.POST.get('optB'+str(i)))
                data_opC.append(request.POST.get('optC'+str(i)))
                data_opD.append(request.POST.get('optD'+str(i)))
        
        for i in range(0,len(data_que)):
            q = Question()
            q.que = data_que[i]
            q.ans = data_ans[i]
            q.opA = data_opA[i]
            q.opB = data_opB[i]
            q.opC = data_opC[i]
            q.opD = data_opD[i]
            q.ex_id = exam
            q.save()
                    

        print("Q = "+str(data_que))
    return render(request,'teacher-set-paper.html',params)