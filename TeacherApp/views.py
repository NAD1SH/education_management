from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import *
from .models import *
from django.contrib import messages
from AdminApp.models import Exam, Room, Message
from datetime import date, datetime
from .access import mrng_access_allowed, evng_access_allowed
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.views.generic import TemplateView, View
from datetime import timedelta, datetime
import os
from django import template
register = template.Library()
from .mixins import TeacherRequiredMixin, LoginRequiredMixin


# Create your views here.
class HomePage(TeacherRequiredMixin, View):
    template_name = 'Teacher/home.html'

    def get(self, request):
        mrng_time = mrng_access_allowed()
        evng_time = evng_access_allowed()
        context = {
            'mrng_time': mrng_time,
            'evng_time': evng_time
        }
        return render(request, self.template_name, context)


class MrngAttendence(TeacherRequiredMixin, View):
    def post(self, request):
        Attend = request.POST['mrng']
        Date = date.today()
        user = request.user.id
        user = Teacher.objects.get(user=user)
        if TeacherAttendence.objects.filter(teacher=user, date=Date).exists() == False:
            addAttendence = TeacherAttendence(
                teacher=user, date=Date, mrngattendence=Attend)
            addAttendence.save()
            messages.success(request, 'Morning Attendence Has Been Marked..')
            return redirect('TrHome')
        else:
            messages.success(
                request, 'You Already Marked Your Attendence. :( ')
            return redirect('TrHome')


class EvngAttendence(TeacherRequiredMixin, View):
    def post(self, request):
        Attend = request.POST['evng']
        Date = date.today()
        user = request.user.id
        user = Teacher.objects.get(user=user)

        if TeacherAttendence.objects.filter(teacher=user, date=Date).exists():
            if TeacherAttendence.objects.filter(teacher=user, date=Date, evngattendence=False):
                trAtt = TeacherAttendence.objects.get(teacher=user, date=Date)
                trAtt.teacher = trAtt.teacher
                trAtt.date = trAtt.date
                trAtt.mrngattendence = trAtt.mrngattendence
                trAtt.evngattendence = Attend
                trAtt.save()
                messages.success(
                    request, 'Evening Attendence Has Been Marked..')
                return redirect('TrHome')
            else:
                messages.success(
                    request, 'You Already Marked Your Attendence. :( ')
                return redirect('TrHome')
        else:
            if TeacherAttendence.objects.filter(teacher=user, date=Date, evngattendence=True).exists() == False:
                addAttendence = TeacherAttendence(
                    teacher=user, date=Date, evngattendence=Attend)
                addAttendence.save()
                messages.success(
                    request, 'Evening Attendence Has Been Marked..')
                return redirect('TrHome')
            else:
                messages.success(
                    request, 'You Already Marked Your Attendence. :( ')
                return redirect('TrHome')


class AddMaterial(TeacherRequiredMixin, View):
    def get(self, request):
        current_user = request.user.id
        current_user = Teacher.objects.get(user=current_user)
        material = CourseMaterial.objects.filter(teacher = current_user)
        form = MaterialForm()

        context = {
            'form': form,
            'fields': material
        }
        return render(request, 'Teacher/uploads.html', context)

    def post(self, request):
        current_user = request.user.id
        current_user = Teacher.objects.get(user=current_user)

        form = MaterialForm(request.POST)

        Title = request.POST['title']
        Description = request.POST['description']
        File = request.FILES['material']
        upload = CourseMaterial(
            teacher=current_user, title=Title, description=Description, material=File)
        upload.save()
        messages.success(request, 'New File Has Been Uploaded...')
        return redirect('upload')


class EditMaterial(TeacherRequiredMixin, View):
    template_name = 'Teacher/CRUD/edit_uploads.html'

    def get(self, request, id):
        material = CourseMaterial.objects.get(pk = id)
        context = {
            'material' : material,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        material = CourseMaterial.objects.get(pk = id)
        
        title = request.POST['title']
        description = request.POST['description']
        
        material.title = title
        material.description = description
        material.save()
        messages.success(request, 'Material Updated successfuly')
        return redirect('upload')


class DeleteMaterial(TeacherRequiredMixin, View):
    def get(self, request, id):
        material = CourseMaterial.objects.get(pk = id)
        material.delete()
        return redirect('upload')


class TeacherProfile(TeacherRequiredMixin, View):
    template_name = 'Teacher/profile.html'

    def get(self, request):
        user = request.user.id
        teacher_user = Teacher.objects.get(user = user)
        context = {
            'teacher_user' : teacher_user
        }
        return render(request, self.template_name, context)


class StudentList(TeacherRequiredMixin, View):
    def get(self, request):
        student = Student.objects.all()
        context = {
            'std': student
        }
        return render(request, 'Teacher/student_list.html', context)


def markpdf(request, id):
    name = Student.objects.get(pk=id)
    mark = Mark.objects.filter(student=id)
    semester = Exam.objects.filter(course=name.course)
    data = []
    Fr = 0
    for i in semester:
        total = 0
        grade = ''
        Fr += 1
        data.append([['', i.title, ''], ['Subject', 'Mark', 'Grade']])
        for m in mark:
            if i.id == m.exam.id:
                total = total+m.mark
                data[Fr-1].append([m.subject, m.mark, m.grade])

        if total >= 500:
            grade = 'A'
        elif total >= 430:
            grade = 'B'
        elif total >= 350:
            grade = 'C'
        elif total >= 280:
            grade = 'D'
        else:
            grade = 'F'
        data[Fr-1].append(['Total Mark ', '', str(total)])
        data[Fr-1].append(['Toal Grade', '', grade])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Report_Card.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []
    for d in data:
        story.append(Table(d))
    for s in story:
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        s.setStyle(style)
    doc.build(story)
    return response


class AddMark(TeacherRequiredMixin, View):
    template_name = 'Teacher/add_mark.html'

    def get(self, request):
        form = MarkForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studentList')
        else:
            return redirect('addMark')


class MarkList(TeacherRequiredMixin, View):
    template_name = 'Teacher/mark_list.html'

    def get(self, request, id):
        name = Student.objects.get(pk=id)
        mark = Mark.objects.filter(student=id)
        semester = Exam.objects.filter(course=name.course)
        total = {}
        for i in semester:
            add = 0
            addMark = Mark.objects.filter(student=id, exam=i.id)
            for j in addMark:
                add += j.mark
            total[i.title] = add

        context = {
            'name': name,
            'mark': mark,
            'sem': semester,
            'total': total
        }
        return render(request, self.template_name, context)


class SentNotification(TeacherRequiredMixin, View):
    template_name = 'Teacher/sent_notification.html'

    def get(self, request):
        form = NotificationForm()
        context = {
            'form' : form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_id = request.user.id
        Sender = Teacher.objects.get(user=user_id)
        Reci = request.POST['recipient']
        Recipient = Student.objects.get(pk=Reci)
        Message = request.POST['message']
        Schedule_Time = request.POST['scheduled_time']
        convert_time = datetime.fromisoformat(Schedule_Time)
        valid_time = str(convert_time + timedelta(hours=24))
        user = Notification.objects.create(sender=Sender, recipient=Recipient, message=Message,
                                           scheduled_time=Schedule_Time, scheduled_upto=valid_time)
        messages.info(request, 'Message Has Been Sended.... :)')
        return redirect('notificationList')
    

class NotificationList(TeacherRequiredMixin, View):
    template_name = 'Teacher/notification_list.html'
    
    def get(self, request):
        user_id = request.user.id
        Sender = Teacher.objects.get(user = user_id)
        notitfication = Notification.objects.filter(sender = Sender)

        context = {
            'notitfication' : notitfication
        }
        return render(request, self.template_name, context)


class EditNotification(TeacherRequiredMixin, View):
    template_name = 'Teacher/CRUD/edit_notification.html'

    def get(self, request, id):
        notificaton = Notification.objects.get(pk = id)
        student = Student.objects.all()
        scheduled_time = notificaton.scheduled_time + timedelta(hours=5, minutes=30)
        alter_time = scheduled_time.strftime('%Y-%m-%dT%H:%M')

        context = {
            'notificaton' : notificaton,
            'student' : student,
            'scheduled_time' : alter_time
        }
        return render(request, self.template_name, context)


    def post(self, request, id):
        notificaton = Notification.objects.get(pk = id)

        Reci = request.POST['recipient']
        Recipient = Student.objects.get(pk=Reci)
        Message = request.POST['message']
        Schedule_Time = request.POST['scheduled_time']
        convert_time = datetime.fromisoformat(Schedule_Time)
        valid_time = str(convert_time + timedelta(hours=24))

        notificaton.recipient = Recipient
        notificaton.message = Message
        notificaton.scheduled_time = Schedule_Time
        notificaton.scheduled_upto = valid_time
        notificaton.save()
        messages.success(request, 'Notification Updated Successfuly')
        return redirect('notificationList')


class DeleteNotification(TeacherRequiredMixin, View):
    def get(self, request, id):
        notificaton = Notification.objects.get(pk = id)
        notificaton.delete()
        messages.success(request, 'Notification Deleted Successfuly :(')
        return redirect('notificationList')
    

class SentAnnouncement(TeacherRequiredMixin, View):
    template_name = 'Teacher/sent_announcement.html'

    def get(self, request):
        form = AnnouncementForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_id = request.user.id
        Sender = Teacher.objects.get(user=user_id)
        Message = request.POST['message']
        current_datetime = datetime.now()
        Schedule_Time = current_datetime
        valid_time = str(Schedule_Time + timedelta(hours=24))
        user = Announcement.objects.create(
            sender=Sender, message=Message, scheduled_time=Schedule_Time, scheduled_upto=valid_time)
        user.save()
        messages.info(request, 'Message Has Been Sended.... :)')
        return redirect('annoucementList')


class AnnouncementList(TeacherRequiredMixin, View):
    template_name = 'Teacher/annoucement_list.html'
    date_time = datetime.now()

    def get(self, request):
        user_id = request.user.id
        Sender = Teacher.objects.get(user = user_id)
        del_announcement = Announcement.objects.filter(scheduled_upto__lt = self.date_time)
        for i in del_announcement:
            i.delete()
        annoucement = Announcement.objects.filter(sender = Sender)    
        context = {
            'annoucement' : annoucement
        }
        return render (request, self.template_name, context)


class EditAnnouncement(TeacherRequiredMixin, View):
    template_name = 'Teacher/CRUD/edit_annoucement.html'

    def get(self, request, id):
        announcement = Announcement.objects.get(pk = id)
        context = {
            'announcement' : announcement
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        announcement = Announcement.objects.get(pk = id)
        Message = request.POST['message']
        announcement.message = Message
        announcement.save()
        messages.success(request, 'Annoucement Updated Successfuly')
        return redirect('annoucementList')


class DeleteAnnouncement(TeacherRequiredMixin, View):
    def get(self, request, id):
        announcement = Announcement.objects.get(pk = id)
        announcement.delete()
        messages.success(request, 'Annoucement Deleted Successfuly :( ')
        return redirect('annoucementList')
    

class ShowChatRooms(TeacherRequiredMixin, View):
    template_name = 'Teacher/room_list.html'

    def get(self, request):
        rooms = Room.objects.all()
        context = {
            'rooms': rooms
        }
        return render(request, self.template_name, context)


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
