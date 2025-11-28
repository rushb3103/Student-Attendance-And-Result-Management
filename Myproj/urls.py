"""Myproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from urllib import request
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.login),
    path('register',views.register),
    path('contact',views.contact),
    path('view-attendance',views.calendar),
    # path('upcoming-exam',views.upcoming),
    path('admin/panel',views.adminpanel),
    path('admin/signup-request',views.adminsignuprequest),
    path('user/panel',views.userpanel),
    path('user/attend-exam',views.userattendexam),
    path('user/attendance-report',views.userattendancereport),
    path('user/scan-attendance',views.userscanattendance),
    path('user/upcoming-exam',views.userupcomingexam),
    path('user/exam-report',views.userexamreport),
    path('admin/student-table',views.adminstudenttable),
    path('admin/teacher-table',views.adminteachertable),
    path('teacher/panel',views.teacherpanel),
    path('teacher/attendance-report',views.teacherattendancereport),
    path('teacher/exam-report',views.teacherexamreport),
    path('teacher/mark-attendance',views.teachermarkattendance),
    path('teacher/signup-requests',views.teachersignuprequest),
    path('teacher/student-details',views.teacherstudenttable),
    path('teacher/view-attendance',views.teacherviewattendance),
    path('teacher/view-result',views.teacherviewresult),
    path('teacher/upcoming-exam',views.teacherupcomingexam),
    path('teacher/create-paper',views.teachercreatepaper),
    path('teacher/edit-paper',views.teachereditpaper),
]
