from django.contrib import admin
from myapp.models import *

# Register your models here.
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Teacher)

admin.site.register(Attendance)