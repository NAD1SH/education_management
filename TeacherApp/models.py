from django.db import models
from AdminApp.models import Courses, Exam, Subject, Teacher, Student

# Create your models here.

class CourseMaterial(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField()
    material = models.FileField(upload_to = 'Course_Material/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
   
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    mark = models.DecimalField(max_digits=4, decimal_places=2)
    grade = models.CharField(max_length=2, blank=True)

    def save(self, *args, **kwargs):

        if self.mark >= 90:
            self.grade = 'A'
        elif self.mark >= 80:
            self.grade = 'B'
        elif self.mark >= 70:
            self.grade = 'C'
        elif self.mark >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student.name + ' ' +'[ ' + self.subject.name + ' ]'
    
class ClassPerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    point = models.CharField(max_length=20)

    def __str__(self):
        return self.student


class TeacherAttendence(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    mrngattendence = models.BooleanField(default=False)
    evngattendence = models.BooleanField(default=False)


class Notification(models.Model):
    sender = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Student, related_name='received_notifications', on_delete=models.CASCADE)
    message = models.TextField()
    scheduled_time = models.DateTimeField()
    scheduled_upto = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.message
    

class Announcement(models.Model):
    sender = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.TextField()
    scheduled_time = models.DateTimeField()
    scheduled_upto = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.message + ' ' + 'Announcement'