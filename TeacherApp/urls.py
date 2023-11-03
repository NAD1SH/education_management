from django.urls import path
from . import views

urlpatterns = [
    path('Home/', views.HomePage.as_view(), name='TrHome'),

    path('Uploadmaterial/', views.AddMaterial.as_view(), name="upload"),
    path('edit_material/<int:id>/', views.EditMaterial.as_view(), name='editMaterial'),
    path('delete_material/<int:id>/', views.DeleteMaterial.as_view(), name='deleteMaterial'),

    path('Profile/', views.TeacherProfile.as_view(), name='profile'),
    path('StudentList/', views.StudentList.as_view(), name='studentList'),
    path('MarkList/<int:id>', views.MarkList.as_view(), name='markList'),
    path('AddMark/', views.AddMark.as_view(), name='addMark'),
    path('mrngAttendence/', views.MrngAttendence.as_view(), name='mrng'),
    path('evngAttendence/', views.EvngAttendence.as_view(), name='evng'),

    path('dowMark/<int:id>', views.markpdf, name='mark_pdf'),
    path('sent_notification/', views.SentNotification.as_view(), name='sent_notification'),
    path('notification_list/', views.NotificationList.as_view(), name='notificationList'),
    path('edit_notification/<int:id>/', views.EditNotification.as_view(), name='editNotification'),
    path('delete_notification/<int:id>/', views.DeleteNotification.as_view(), name='deleteNotification'),

    path('announcement/', views.SentAnnouncement.as_view(), name='sent_announcement'),
    path('annoucement_list', views.AnnouncementList.as_view(), name='annoucementList'),
    path('edit_announcement/<int:id>/', views.EditAnnouncement.as_view(), name='editAnnoucement'),
    path('delete_announcement/<int:id>/', views.DeleteAnnouncement.as_view(), name='deleteAnnouncement'),

    path('rooms/', views.ShowChatRooms.as_view(), name='TrchatRooms'),
    path('<slug:slug>/', views.ChatRoom.as_view(), name='TrchatRoom'),
]
