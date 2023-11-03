from django.contrib import admin
from .models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
        model = Student
        list_display = ['id', 'name']    
admin.site.register(Student, StudentAdmin)


class TeacherAdmin(admin.ModelAdmin):
        model = Teacher
        list_display = ['id', 'name']  
admin.site.register(Teacher, TeacherAdmin)


class CourseAdmin(admin.ModelAdmin):
        model = Courses
        list_display = ['id', 'course']
admin.site.register(Courses, CourseAdmin)

admin.site.register(Exam)
admin.site.register(Subject)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)

admin.site.register(Room)
admin.site.register(Message)