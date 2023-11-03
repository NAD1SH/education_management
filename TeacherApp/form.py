from django import forms
from .models import *

class MaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'description', 'material']



class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'exam', 'subject', 'mark']

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['recipient', 'message']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['message']
