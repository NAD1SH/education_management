from django.db import models
from UserApp.models import UserProfile

# Create your models here.


class Courses(models.Model):
    course = models.CharField(max_length=40)
    discription = models.TextField()
    fee = models.CharField(max_length=30)

    def __str__(self):
        return self.course
    
    class Meta:
        verbose_name_plural = 'Course'

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=20, unique=True, default='STD')
    name = models.CharField(max_length=50)
    batch_start = models.CharField(max_length=50)
    batch_end = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Student'

    def __str__(self):
        return self.name

class Teacher(models.Model):    
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=12, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Teacher'

    def __str__(self):
        return self.name

class Exam(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title+ '[ '+ self.course.course+ ' ]'   
    
class Subject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name



# Student and Teacher Chat
class Room(models.Model):
    room = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, max_length=20)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.room

class Message(models.Model):
    message = models.CharField(max_length=30)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('create_on',)