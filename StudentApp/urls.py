from django.urls import path
from . import views

urlpatterns = [
    path('Home/', views.HomePage.as_view(), name='SdHome'),
    path('Profile/', views.StudentProfile.as_view(), name='stdProfile'),
    path('Materials/', views.StudyMaterial.as_view(), name='courserMaterial'),
    path('VideoPlayer/<int:id>', views.VideoPlayer.as_view(), name='videoPlayer'),
    path('Announcement/', views.ShowNotification.as_view(), name='notify'),
    path('Render_Notification/', views.RenderNotification.as_view(), name=''),
    path('delete_notification/<int:id>', views.DeleteNotification.as_view(), name='delete_notification'),
    path('Render_Announcement/', views.RenderAnnouncement.as_view(), name='renderAnnouncement'),
    path('Video_library/', views.videoLibrary.as_view(), name='library'),
    path('<slug:slug>/', views.ChatRoom.as_view(), name='StChatRoom')
]

