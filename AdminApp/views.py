from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from UserApp.models import UserProfile
from .form import *
from .serialiazer import StudentSerializer, TeacherSerializer, UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib import messages
from rest_framework.response import Response
from TeacherApp.models import TeacherAttendence
import pandas as pd
from datetime import datetime, date, timedelta
import pyotp
from Project.settings import RECAPTCHA_SECRET_KEY
import requests
from django.template.loader import get_template
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from AdminApp.mixins import AdminRequiredMixin, admin_required, LoginRequiredMixin


# Create your views here.
class HomePage(AdminRequiredMixin, TemplateView):
    template_name = 'Admin/home.html'


@admin_required
def StudentRegisterPage(request):
    if request.method == 'POST':
        Username = request.POST['username']
        Password = request.POST['password']
        Email = request.POST['email']
        Reg_No = request.POST['reg_no']
        Name = request.POST['name']
        Batch_Start = request.POST['batch_start']
        Batch_End = request.POST['batch_end']
        Course = request.POST['course']
        Contact = request.POST['contact']
        country = request.POST['country']
        state = request.POST['state']
        district = request.POST['district']
        recaptcha_token = request.POST['token']
        Role = 'student'

        CountrY = Country.objects.get(pk=country)
        StatE = State.objects.get(pk=state)
        DistricT = District.objects.get(pk=district)
        course_inst = Courses.objects.get(pk=Course)

        if UserProfile.objects.filter(username=Username).exists():
            messages.error(request, 'This Username Already Exist')
            return redirect('studentRegister')

        if UserProfile.objects.filter(email=Email).exists():
            messages.error(request, 'This Email Address Already Exist')
            return redirect('studentRegister')

        if Student.objects.filter(reg_no=Reg_No).exists():
            messages.error(request, 'This Register Number Already Exist')
            return redirect('studentRegister')

        if Password.isalnum() == True:
            messages.error(
                request, 'Password Must Want To Contain number and special character...')
            return redirect('studentRegister')

        data = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_token
        }

        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        if result['success']:
            user = UserProfile.objects.create(
                username=Username, password=Password, role=Role,  email=Email,)
            user.save()
            student = Student(user=user, name=Name, reg_no=Reg_No, course=course_inst, batch_start=Batch_Start,
                              batch_end=Batch_End, country=CountrY, state=StatE, district=DistricT, contact=Contact)
            student.save()
            messages.success(
                request, 'New Student Has Been Successfully Registered....')
            return redirect('studentRegister')
        else:
            messages.success(
                request, 'Recapcha Token Athentication Has Failed....')
            return redirect('studentRegister')
    else:
        form = StudentForm()
        countries = Country.objects.all()

        context = {
            'form': form,
            'countries': countries
        }
        return render(request, 'Admin/Student_register.html', context)


@admin_required
def TeacherRegisterPage(request):
    if request.method == 'POST':
        role = 'teacher'
        Username = request.POST['username']
        Password = request.POST['password']
        Email = request.POST['email']
        Reg_No = request.POST['reg_no']
        Name = request.POST['name']
        Phone = request.POST['contact']
        country = request.POST['country']
        state = request.POST['state']
        district = request.POST['district']
        recaptcha_token = request.POST['token']

        CountrY = Country.objects.get(pk=country)
        StatE = State.objects.get(pk=state)
        DistricT = District.objects.get(pk=district)

        if UserProfile.objects.filter(username=Username).exists():
            messages.error(request, 'This Username Already Exist')
            return redirect('teacherRegister')

        if Teacher.objects.filter(reg_no=Reg_No).exists():
            messages.error(request, 'This Register Number Already Exist')
            return redirect('teacherRegister')

        if UserProfile.objects.filter(email=Email).exists():
            messages.error(request, 'This Email Already Exist')
            return redirect('teacherRegister')

        data = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_token
        }

        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        if result['success']:
            user = UserProfile(username=Username,
                               password=Password, role=role,  email=Email)
            user.save()
            teacher = Teacher(user=user, reg_no=Reg_No, name=Name,
                              contact=Phone, country=CountrY, state=StatE, district=DistricT)
            teacher.save()
            messages.success(
                request, 'New Teacher Has Been Successfully Registered....')
            return redirect('teacherRegister')
        else:
            messages.success(
                request, 'Recapcha Token Athentication Has Failed....')
            return redirect('teacherRegister')
    else:
        countries = Country.objects.all()
        form = TeacherForm()
        context = {
            'form': form,
            'countries': countries
        }
        return render(request, 'Admin/Teacher_register.html', context)


class GetStates(AdminRequiredMixin, View):
    def get(self, request):
        country_id = request.GET.get('country_id')
        states = State.objects.filter(country_id=country_id).values('id', 'name')
        return JsonResponse({'states': list(states)})


class GetDistricts(AdminRequiredMixin, View):
    def get(self, request):
        state_id = request.GET.get('state_id')
        districts = District.objects.filter(
            state_id=state_id).values('id', 'name')
        return JsonResponse({'districts': list(districts)})


class CountryDetail(AdminRequiredMixin, View):
    template_name = 'Admin/country_detail.html'

    def get(self, request):
        country_form = CountryForm()
        state_form = StateForm()
        district_form = DistrictForm()
        countries = Country.objects.all()

        context = {
            'country_form': country_form,
            'state_form': state_form,
            'district_form': district_form,
            'countries': countries
        }

        return render(request, self.template_name, context)


class AddCountry(AdminRequiredMixin, View):
    def post(self, request):
        country_form = CountryForm(request.POST)
        if country_form.is_valid():
            country_form.save()
            messages.success(request, 'New Country Has Been Added')
            return redirect('countryDetail')
        else:
            messages.error(request, 'Something Went Wrong')
            return redirect('countryDetail')


class CountryList(AdminRequiredMixin, View):
    template_name = "Admin/country_list.html"

    def get(self, request):
        country = Country.objects.all()

        context = {
            'country': country
        }
        return render(request, self.template_name, context)


class EditCountry(AdminRequiredMixin, View):
    template_name = 'Admin/CRUD/edit_country.html'

    def get(self, request, id):
        country = Country.objects.get(pk=id)
        context = {
            'country': country
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        country = Country.objects.get(pk=id)
        name = request.POST['name']
        country.name = name
        country.save()
        messages.success(request, 'Country Update Successfuly')
        return redirect('countryList')
    

class DeleteCountry(AdminRequiredMixin, View):
    def get(self, request, id):
        country = Country.objects.get(pk = id)
        country.delete()
        messages.success(request, 'Country Delete Successfuly')
        return redirect('countryList')


class AddState(AdminRequiredMixin, View):
    def post(self, request):
        state_form = StateForm(request.POST)
        if state_form.is_valid():
            state_form.save()
            messages.success(request, 'New State Has Been Added')
            return redirect('countryDetail')
        else:
            messages.error(request, 'Something Went Wrong')
            return redirect('countryDetail')


class StateList(AdminRequiredMixin, View):
    template_name = "Admin/state_list.html"

    def get(self, request):
        countrys = Country.objects.all()
        states = State.objects.all()
        context = {
            'states': states,
            'countrys': countrys
        }
        return render(request, self.template_name, context)


class EditState(AdminRequiredMixin, View):
    template_name = 'Admin/CRUD/edit_state.html'

    def get(self, request, id):
        countrys = Country.objects.all()
        state = State.objects.get(pk=id)
        context = {
            'state': state,
            'country': countrys
        }
        return render(request, 'Admin/CRUD/edit_state.html', context)

    def post(self, request, id):
        state = State.objects.get(pk=id)
        name = request.POST['name']
        country = request.POST['country']
        country = Country.objects.get(pk=country)

        state.name = name
        state.country = country
        state.save()
        messages.success(request, 'State Updated Successfuly.')
        return redirect('stateList')
    

class DeleteState(AdminRequiredMixin, View):
    def get(self, request, id):
        state = State.objects.get(pk = id)
        state.delete()
        messages.success(request, 'State Delete Successfuly.')
        return redirect('stateList')


class AddDistrict(AdminRequiredMixin, View):
    def post(self, request):
        name = request.POST['name']
        country = request.POST['country']
        state = request.POST['state']

        CountrY = Country.objects.get(pk=country)
        StatE = State.objects.get(pk=state)

        district = District(name=name, country=CountrY, state=StatE)
        district.save()
        messages.success(request, 'New District Has Been Added')
        return redirect('countryDetail')


class DistrictList(AdminRequiredMixin, View):
    template_name = "Admin/district_list.html"

    def get(self, request):
        countrys = Country.objects.all()
        states = State.objects.all()
        districts = District.objects.all()
        context = {
            'districts': districts,
            'countrys': countrys,
            'states': states
        }
        return render(request, self.template_name, context)


class EditDistrict(AdminRequiredMixin, View):
    template_name = 'Admin/CRUD/edit_district.html'

    def get(self, request, id):
        district = District.objects.get(pk=id)
        countries = Country.objects.all()
        states = State.objects.all()

        context = {
            'countries': countries,
            'states': states,
            'district': district
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        district = District.objects.get(pk=id)
        name = request.POST['name']
        district.name = name
        district.save()
        messages.success(request, 'District Updated Successfuly.')
        return redirect('districtList')

class DeleteDistrict(AdminRequiredMixin, View):
    def get(self, request, id):
        district = District.objects.get(pk = id)
        district.delete()
        messages.success(request, 'District Delete Successfuly.')
        return redirect('districtList')


class TeacherAttendenceReport(AdminRequiredMixin, View):
    template_name = 'Admin/teacher_attendence.html'

    def get(self, request):
        attendence = TeacherAttendence.objects.all()
        context = {
            'att': attendence,
        }
        return render(request, self.template_name, context)


class StudentCourseCompletionList(AdminRequiredMixin, View):
    template_name = 'Admin/course_completions_list.html'

    def get(self, request):
        student = Student.objects.all()
        context = {
            'std': student
        }
        return render(request, self.template_name, context)


class CourseCompletionCertificate(AdminRequiredMixin, View):
    template_name = 'Admin/completion_pdf.html'

    def get(self, request, id):
        student = Student.objects.get(pk=id)
        Date = date.today()
        context = {
            'std': student,
            'date': Date.strftime("%x"),
            'std_id': student.id
        }
        return render(request, self.template_name, context)


# ----------------- excel export ------------------- #

def Student_Export_Data(request):
    obj = Student.objects.all()
    std = []
    for i in obj:
        std.append({
            "Register No": i.reg_no,
            "Name": i.name,
            "Email": i.user.email,
            "Course": i.course,
            "Contact": i.contact,
            "Country": i.country,
            "State": i.state,
            "District": i.district,
            "Batch Start": i.batch_start,
            "Batch End": i.batch_end,
        })

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Student_List.xlsx'

    pd.DataFrame(std).to_excel(response, index=False, sheet_name='Sheet1')

    return response


def Teacher_Export_Data(request):
    obj = Teacher.objects.all()
    tr = []
    for i in obj:
        tr.append({
            "Register No": i.reg_no,
            "Name": i.name,
            "Email": i.user.email,
            "Contact": i.contact,
            "Country": i.country,
            "State": i.state,
            "District": i.district,
        })

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Student_List.xlsx'

    pd.DataFrame(tr).to_excel(response, index=False, sheet_name='Sheet1')
    return redirect('teacherList')


class GeneratePDF(AdminRequiredMixin, View):
    template_name = 'Admin/completion_pdf.html'

    def get(self, request, id):
        student = Student.objects.get(pk=id)
        Date = date.today()
        context = {
            'std': student,
            'date': Date.strftime("%x"),
        }

        template = get_template(self.template_name)
        html = template.render(context)

        pdf_file = HTML(string=html).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificate.pdf"'

        return response


# show student list, delete, update, details template rendering
class List_Student(AdminRequiredMixin, View):
    template_name = 'Admin/Student_List.html'

    def get(self, request):
        student = Student.objects.all()
        context = {
            'std': student
        }
        return render(request, self.template_name, context)
    

class RemovedStudentList(AdminRequiredMixin, View):
    template_name = 'Admin/removed_student.html'

    def get(self, request):
        student = Student.objects.all()
        context = {
            'std': student
        }
        return render(request, self.template_name, context)


class Edit_Student(AdminRequiredMixin, View):
    template_name = 'Admin/CRUD/edit_student.html'

    def get(self, request, id):
        student = Student.objects.get(pk=id)
        courses = Courses.objects.all()
        countries = Country.objects.all()
        context = {
            'student': student,
            'courses': courses,
            'countries': countries
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        student = Student.objects.get(pk=id)
        Email = request.POST['email']
        Reg_No = request.POST['reg_no']
        Name = request.POST['name']
        Phone = request.POST['contact']
        Batch_Start = request.POST['batch_start']
        Batch_End = request.POST['batch_end']
        Course = request.POST['course']
        country = request.POST['country']
        state = request.POST['state']
        district = request.POST['district']

        course_inst = Courses.objects.get(pk=Course)
        CountrY = Country.objects.get(pk=country)
        StatE = State.objects.get(pk=state)
        DistricT = District.objects.get(pk=district)

        user_email = UserProfile.objects.filter(email=Email).first()
        user_reg = Student.objects.filter(reg_no=Reg_No).first()

        if user_reg is not None:
            if user_reg.id == student.id:
                user_reg.reg_no = Reg_No
            else:
                messages.error(request, 'Register Number Already Exist :(')
                return redirect('editStudent', id=id)
        else:
            student.reg_no = Reg_No

        if user_email is not None:
            if user_email.id == student.user.id:
                user_email.email = Email
                user_email.save()
            else:
                messages.error(request, 'Email Address Already Exist :(')
                return redirect('editStudent', id=id)
        else:
            user_profile = UserProfile.objects.get(pk=student.user.id)
            user_profile.email = Email
            user_profile.save()

        student.name = Name
        student.contact = Phone
        student.batch_start = Batch_Start
        student.batch_end = Batch_End
        student.course = course_inst
        student.country = CountrY
        student.state = StatE
        student.district = DistricT
        student.save()
        messages.success(request, 'Student Updated Successfuly')
        return redirect('liststudent')


class Delete_Student(AdminRequiredMixin, View):
    def get(self, request, id):
        student = Student.objects.get(pk=id)
        user = UserProfile.objects.get(pk=student.user.id)
        user.is_active = False
        user.save()
        return redirect('liststudent')


class List_Teacher(AdminRequiredMixin, View):
    template_name = 'Admin/Teacher_List.html'

    def get(self, request):
        teacher = Teacher.objects.all()
        context = {
            'teacher': teacher
        }
        return render(request, self.template_name, context)


class RemovedTeacherList(AdminRequiredMixin, View):
    template_name = 'Admin/removed_teacher.html'

    def get(self, request):
        teacher = Teacher.objects.all()
        context = {
            'teacher': teacher
        }
        return render(request, self.template_name, context)


class Edit_Teacher(AdminRequiredMixin, View):
    template_name = 'Admin/CRUD/edit_teacher.html'

    def get(self, request, id):
        teacher = Teacher.objects.get(pk=id)
        countries = Country.objects.all()
        context = {
            'countries': countries,
            'teacher': teacher
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        teacher = Teacher.objects.get(pk=id)

        Email = request.POST['email']
        Reg_No = request.POST['reg_no']
        Name = request.POST['name']
        Phone = request.POST['contact']
        country = request.POST['country']
        state = request.POST['state']
        district = request.POST['district']

        CountrY = Country.objects.get(pk=country)
        StatE = State.objects.get(pk=state)
        DistricT = District.objects.get(pk=district)

        user_email = UserProfile.objects.filter(email=Email).first()
        user_reg = Teacher.objects.filter(reg_no=Reg_No).first()

        if user_reg is not None:
            if user_reg.id == teacher.id:
                user_reg.reg_no = Reg_No
            else:
                messages.error(request, 'Register Number Already Exist :(')
                return redirect('editTeacher', id=id)
        else:
            teacher.reg_no = Reg_No

        if user_email is not None:
            if user_email.id == teacher.user.id:
                user_email.email = Email
                user_email.save()
            else:
                messages.error(request, 'Email Address Already Exist :(')
                return redirect('editTeacher', id=id)
        else:
            user_profile = UserProfile.objects.get(pk=teacher.user.id)
            user_profile.email = Email
            user_profile.save()

        teacher.name = Name
        teacher.contact = Phone
        teacher.country = CountrY
        teacher.state = StatE
        teacher.district = DistricT
        teacher.save()

        messages.success(request, 'Teacher Updated Successfuly')
        return redirect('teacherList')


class Remove_Teacher(AdminRequiredMixin, View):
    def get(self, request, id):
        teacher = Teacher.objects.get(pk=id)
        user = UserProfile.objects.get(pk=teacher.user.id)
        user.is_active = False
        user.save()
        return redirect('teacherList')


class AcademicEvent(AdminRequiredMixin, View):
    template_name = 'Admin/academic_event.html'

    def get(self, request):
        course = Courses.objects.all()
        semester = Exam.objects.all()
        sub = Subject.objects.all()
        context = {
            'course': course,
            'sem': semester,
            'sub': sub
        }
        return render(request, self.template_name, context)


class AddCourse(AdminRequiredMixin, View):
    template_name = 'Admin/add_course.html'

    def get(self, request):
        form = CourseForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academinEvent')


class CourseList(AdminRequiredMixin, View):
    template_name = 'Admin/course_list.html'

    def get(self, request):
        courses = Courses.objects.all()
        context = {
            'courses': courses
        }
        return render(request, self.template_name, context)


class EditCourse(AdminRequiredMixin, View):
    template_name = 'Admin/CRUD/edit_course.html'

    def get(self, request, id):
        courses = Courses.objects.get(pk=id)
        context = {
            'courses': courses
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        courses = Courses.objects.get(pk=id)
        Course = request.POST['course']
        Discription = request.POST['description']

        courses.course = Course
        courses.discription = Discription
        courses.save()
        messages.success(request, 'Course Successfuly Updated ..')
        return redirect('courseList')

class DeleteCourse(AdminRequiredMixin, View):
    def get(self, request, id):
        course = Courses.objects.get(pk = id)
        course.delete()
        print('delete')
        messages.success(request, 'Course Delete Successfuly')
        return redirect('courseList')

class AddExam(AdminRequiredMixin, View):
    template_name = 'Admin/add_exam.html'

    def get(self, request):
        form = ExamForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        Course = request.POST['course']
        Date = request.POST['date']
        Title = request.POST['title']

        Course = Courses.objects.get(pk=Course)
        Exam.objects.create(course=Course, date=Date, title=Title)
        return redirect('academinEvent')


class ExamList(AdminRequiredMixin, View):
    template_name = 'Admin/exam_list.html'

    def get(self, request):
        course = Courses.objects.all()
        exams = Exam.objects.all()

        context = {
            'exams': exams,
            'course': course
        }
        return render(request, self.template_name, context)


class EditExam(AdminRequiredMixin, View):
    template_name = 'Admin/CRUD/edit_exam.html'

    def get(self, request, id):
        exam = Exam.objects.get(pk=id)
        alter_date = exam.date.strftime('%Y-%m-%d')
        context = {
            'exam': exam,
            'alter_date': alter_date
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        exam = Exam.objects.get(pk=id)
        Title = request.POST['title']

        exam.title = Title
        exam.save()
        messages.success(request, 'Exam Title Successfuly Updated')
        return redirect('examList')
    

class DeleteExam(AdminRequiredMixin, View):
    def get(self, request, id):
        exam = Exam.objects.get(pk = id)
        exam.delete()
        messages.success(request, 'Exam Delete Successfuly')
        return redirect('examList')

class AddSubject(AdminRequiredMixin, View):
    template_name = 'Admin/add_subject.html'

    def get(self, request):
        form = SubjectForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('academinEvent')


class SubjectList(AdminRequiredMixin, View):
    template_name = "Admin/subject_list.html"

    def get(self, request):
        subject = Subject.objects.all()
        exam = Exam.objects.all()
        course = Courses.objects.all()
        context = {
            'subject': subject,
            'exam': exam,
            'course': course
        }
        return render(request, self.template_name, context)


class EditSubject(AdminRequiredMixin, View):
    template_name = 'Admin/CRUD/edit_subject.html'

    def get(self, request, id):
        subject = Subject.objects.get(pk=id)
        context = {
            'subject': subject
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        subject = Subject.objects.get(pk=id)
        name = request.POST['name']
        subject.name = name
        subject.save()
        messages.success(request, 'Subject Name Successfuly Updated')
        return redirect('subjectList')
    

class DeleteSubject(AdminRequiredMixin, View):
    def get(self, request, id):
        subject = Subject.objects.get(pk = id)
        subject.delete()
        messages.success(request, 'Subject Delete Successfuly')
        return redirect('subjectList')


# Teacher and Student Chat Module
class AddRoom(AdminRequiredMixin, View):
    template_name = 'Admin/create_room.html'

    def get(self, request):
        form = RoomForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        room_name = request.POST['room']
        Course = request.POST['course']
        Course = Courses.objects.get(pk=Course)
        Slug = room_name.lower()
        Slug = Slug.replace(" ", "")

        if Room.objects.filter(room=room_name, course=Course).exists():
            messages.info(request, 'Room Name Alrady Exist..')
            return redirect('createRoom')
        else:
            Room.objects.create(room=room_name, slug=Slug, course=Course)
            return redirect('chatRooms')


class ShowChatRooms(AdminRequiredMixin, View):
    template_name = 'Admin/room_list.html'

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


# Student serializer
@api_view(['GET'])
def ListStudent(request):
    student = Student.objects.all()
    serializer = StudentSerializer(student, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def CreateStudent(request):
    role = 'student'

    data = request.data

    Username = data.get('username')
    Password = data.get('password')
    Email = data.get('email')
    Reg_No = data.get('reg_no')
    Name = data.get('name')
    Batch = data.get('batch')
    Course = data.get('course')
    Contact = data.get('contact')

    user_serializer = UserSerializer(data={
        "username": Username,
        "password": Password,
        "role": role

    })

    if user_serializer.is_valid():
        std_user = user_serializer.save()
    else:
        return Response({'error': 'invalid user data'}, status=400)

    student_serializer = StudentSerializer(data={
        "user": std_user.id,
        "reg_no": Reg_No,
        "name": Name,
        "email": Email,
        "batch": Batch,
        "course": Course,
        "contact": Contact
    })

    if student_serializer.is_valid():
        student_serializer.save()
        return Response('Created new student to the list')
    else:
        std_user.delete()
        return Response({'error': 'Invalid Profile data'}, status=400)


@api_view(['PUT'])
def UpdateStudent(request, id):
    student = Student.objects.get(pk=id)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('Updated the student detail')
    else:
        return Response("can't save invalid data to database")
    return Response(serializer.data)


@api_view(['DELETE'])
def DeleteStudent(requset, id):
    student = Student.objects.get(pk=id)
    std_user = student.user.id
    user = UserProfile.objects.get(pk=std_user)
    student.delete()
    user.delete()
    return Response('The Student Has Been Delete')


# Teacher serializer
@api_view(['GET'])
def ListTeacher(request):
    teacher = Teacher.objects.all()
    serializer = TeacherSerializer(teacher, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def CreateTeacher(request):
    role = 'teacher'
    data = request.data

    Username = data.get('username')
    Password = data.get('password')
    Reg_No = data.get('reg_no')
    Name = data.get('name')
    Email = data.get('email')
    Phone = data.get('phone')

    user_serializer = UserSerializer(data={
        "username": Username,
        "password": Password,
        "role": role
    })

    if user_serializer.is_valid():
        tr_user = user_serializer.save()
    else:
        return Response({'error': "can't create New Teacher user"}, status=400)

    teacher_serializer = TeacherSerializer(data={
        "user": tr_user.id,
        "reg_no": Reg_No,
        "name": Name,
        "email": Email,
        "contact": Phone,
    })

    if teacher_serializer.is_valid():
        teacher_serializer.save()
        return Response("New Teacher has been created")
    else:
        tr_user.delete()
        return Response({'error': "Can't create new Teacher Profile"}, status=400)


@api_view(['PUT'])
def UpdateTeacher(request, id):
    teacher = Teacher.objects.get(pk=id)
    serializer = TeacherSerializer(teacher, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("The Teacher has been Updated")
    else:
        return Response({'error': "can't Updata Teacher"}, status=400)


@api_view(['DELETE'])
def DeleteTeacher(request, id):
    teacher = Teacher.objects.get(pk=id)
    tr_user = teacher.user.id
    user = UserProfile.objects.get(pk=tr_user)
    teacher.delete()
    user.delete()
    return Response('Teacher Has Been Delete From List')
