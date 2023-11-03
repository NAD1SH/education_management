from django.contrib import admin
from .models import *
# Register your models here.


class CourseMaterialAdmin(admin.ModelAdmin):
        model = CourseMaterial
        list_display = ['title']
admin.site.register(CourseMaterial, CourseMaterialAdmin)

admin.site.register(Mark)
admin.site.register(ClassPerformance)

admin.site.register(TeacherAttendence)

admin.site.register(Notification)

admin.site.register(Announcement)