from django import forms
from .models import *


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course', 'discription']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'title']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room', 'course']

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'
