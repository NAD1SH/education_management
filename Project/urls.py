from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Admin/', include('AdminApp.urls')),
    path('Student/', include('StudentApp.urls')),
    path('Teacher/', include('TeacherApp.urls')),
    path('', include('UserApp.urls')),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
