from django.urls import path
from .import views

urlpatterns = [
    path('Home/', views.HomePage.as_view(), name='home'),
    path('Academic/', views.AcademicEvent.as_view(), name='academinEvent'),

    path('Add_course/', views.AddCourse.as_view(), name='addCourse'),
    path('course_list/', views.CourseList.as_view(), name='courseList'),
    path('edit_course/<int:id>/', views.EditCourse.as_view(), name='editCourse'),
    path('delete_course/<int:id>/', views.DeleteCourse.as_view(), name='deleteCourse'),

    path('Add_Exam/', views.AddExam.as_view(), name='addExam'),
    path('exam_list/', views.ExamList.as_view(), name='examList'),
    path('edit_exam/<int:id>/', views.EditExam.as_view(), name='editExam'),
    path('delete_exam/<int:id>/', views.DeleteExam.as_view(), name='deleteExam'),

    path('Add_Subject/', views.AddSubject.as_view(), name='addSubject'),
    path('subject_list/', views.SubjectList.as_view(), name='subjectList'),
    path('edit_subject/<int:id>/', views.EditSubject.as_view(), name='editSubject'),
    path('delete_subject/<int:id>/', views.DeleteSubject.as_view(), name='deleteSubject'),

    path('Att_report/', views.TeacherAttendenceReport.as_view(), name='AttReort'),
    path('student_list/', views.StudentCourseCompletionList.as_view(), name='course_completion_list'),

    path('Genrate_certificate/<int:id>', views.GeneratePDF.as_view(), name='generate_pdf'),
    path('certificate/<int:id>/', views.CourseCompletionCertificate.as_view(), name='certificate'),

    path('country_detail/', views.CountryDetail.as_view(), name='countryDetail'),
    path('add_country/', views.AddCountry.as_view(), name='add_country'),
    path('country_list/', views.CountryList.as_view(), name='countryList'),
    path('edit_country/<int:id>/', views.EditCountry.as_view(), name='editCountry'),
    path('delete_country/<int:id>/', views.DeleteCountry.as_view(), name='deleteCountry'),

    path('add_state/', views.AddState.as_view(), name='add_state'),
    path('state_list/', views.StateList.as_view(), name='stateList'),
    path('edit_state/<int:id>/', views.EditState.as_view(), name='editState'),
    path('delete_state/<int:id>/', views.DeleteState.as_view(), name='deleteState'),

    path('add_district/', views.AddDistrict.as_view(), name='add_district'),
    path('district_list/', views.DistrictList.as_view(), name='districtList'),
    path('edit_district/<int:id>/', views.EditDistrict.as_view(), name='editDistrict'),
    path('delete_district/<int:id>/', views.DeleteDistrict.as_view(), name='deleteDistrict'),

    path('StudentRegister/', views.StudentRegisterPage, name='studentRegister'),
    path('StudentList/', views.List_Student.as_view(), name='liststudent'),
    path('Edit_Student/<int:id>/', views.Edit_Student.as_view(), name='editStudent'),
    path('Delete_Student/<int:id>/', views.Delete_Student.as_view(), name="DeleteStudent"),
    path('StdExport/', views.Student_Export_Data, name='stdExport'),
    path('RemovedStudent/', views.RemovedStudentList.as_view(), name='removedStudent'),

    path('TeacherRegister/', views.TeacherRegisterPage, name='teacherRegister'),
    path('TeacherList/', views.List_Teacher.as_view(), name='teacherList'),
    path('Edit_Teacher/<int:id>/', views.Edit_Teacher.as_view(), name='editTeacher'),
    path('Delete_Teacher/<int:id>/', views.Remove_Teacher.as_view(), name='DeleteTeacher'),
    path('TrExport/', views.Teacher_Export_Data, name='trExport'),
    path('RemovedTeacher/', views.RemovedTeacherList.as_view(), name='removedTeacher'),

    # chat
    path('create_room/', views.AddRoom.as_view(), name='createRoom'),
    path('rooms/', views.ShowChatRooms.as_view(), name='chatRooms'),
    path('<slug:slug>/', views.ChatRoom.as_view(), name='chatRoom'),

    # dropdown
    path('get/get_states/', views.GetStates.as_view(), name='get_states'),
    path('get/get_districts/', views.GetDistricts.as_view(), name='get_districts'),


    # Student serializer path
    path('StudentList/', views.ListStudent, name='studentList'),
    path('CreateStudent/', views.CreateStudent, name='createStudent'),
    path('UpdateStudent/<int:id>', views.UpdateStudent, name='updateStudent'),
    path('DeleteStudent/<int:id>', views.DeleteStudent, name='deleteStudent'),

    # Teacher serializer path
    path('ListTeacher/', views.ListTeacher, name='listTeacher'),
    path('CreateTeacher/', views.CreateTeacher, name='createTeacher'),
    path('UpdateTeacher/<int:id>', views.UpdateTeacher, name='updateTeacher'),
    path('DeleteTeacher/<int:id>', views.DeleteTeacher, name='deleteTeacher')
]
