from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from TeacherApp.models import CourseMaterial, Notification, Announcement
from AdminApp.models import Room, Student, Message
from datetime import datetime, time, timedelta
from django.core import serializers
import pytz
from django.views.generic import TemplateView, View
from .mixins import StudentRequiredMixin, LoginRequiredMixin

# Create your views here.
class HomePage(StudentRequiredMixin, View):
    template_name = 'Student/home.html'

    def get(self, request):
        user = request.user.id
        student = Student.objects.get(user = user)
        rooms = Room.objects.filter(course = student.course)
        context = {
            'rooms' : rooms
        }
        return render(request, self.template_name, context)


class RenderNotification(StudentRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        std = Student.objects.get(user=user_id)
        current_datetime = datetime.now(pytz.UTC)
        current_datetime = current_datetime + timedelta(hours=5, minutes=30)

        if Notification.objects.filter(recipient=std):
            notification = Notification.objects.filter(recipient=std)
            if notification is not None:
                data = serializers.serialize('json', notification)
                for i in notification:
                    if i.scheduled_upto < current_datetime:
                        del_notify = Notification.objects.get(pk=i.id)
                        del_notify.delete()
                    else:
                        pass
                return JsonResponse(data, safe=False)
            else:
                data = serializers.serialize('json', notification=None)
        else:
            print('there is not notification for you...')
            data = 'None'
            return JsonResponse(data, safe=False)
        

class RenderAnnouncement(StudentRequiredMixin, View):
    def get(self, request):
        announcement = Announcement.objects.all()
        data = serializers.serialize('json', announcement)
        return JsonResponse(data, safe=False)


class StudentProfile(StudentRequiredMixin, View):
    template_name = 'Student/profile.html'

    def get(self, request):
        user = request.user.id
        student_user = Student.objects.get(user = user)
        context = {
            'student_user' : student_user
        }
        return render(request, self.template_name, context)


class StudyMaterial(StudentRequiredMixin, View):
    template_name = 'Student/matrials.html'
    def get(self, request):
        file = CourseMaterial.objects.all()
        context = {
            'files': file
        }
        return render(request, self.template_name , context)


class VideoPlayer(StudentRequiredMixin, View):
    template_name = 'Student/video_player.html'
    def get(self, request, id):
        file = CourseMaterial.objects.get(pk=id)
        context = {
            'file': file
        }
        return render(request, self.template_name , context)


class ShowNotification(StudentRequiredMixin, TemplateView):
    template_name = 'Student/notification.html'


class DeleteNotification(StudentRequiredMixin, View):
    def get(self, request, id):
        notify = Notification.objects.get(pk=id)
        notify.delete()
        return redirect('SdHome')


class videoLibrary(StudentRequiredMixin, View):
    template_name = 'Student/library.html'
    def get(self, request):
        video_materials = CourseMaterial.objects.filter(material__icontains='mp4')
        context = {
            'video' : video_materials
        }
        return render(request, self.template_name , context)
    

class ChatRoom(LoginRequiredMixin, View):
    template_name = 'Admin/chat_room.html'

    def get(self, request, slug):
        chat_room = Room.objects.get(slug=slug)
        messages = Message.objects.filter(room=chat_room)[0:25]

        context = {
            'chat_room': chat_room,
            'messages': messages
        }
        return render(request, self.template_name, context)