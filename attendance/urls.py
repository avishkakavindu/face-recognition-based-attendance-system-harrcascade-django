from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from attendance.views import RegisterView, StudentRegisterAPIView, StudentImageAPIView, TrainView, AttendanceView, AttendanceAPIVIew

urlpatterns = [
    path('', RegisterView.as_view(), name='index'),
    path('register/', StudentRegisterAPIView.as_view(), name='register-api-view'),
    path('student_image/', StudentImageAPIView.as_view(), name='student-image'),
    path('train/', TrainView.as_view(), name='train'),
    path('attendance/', AttendanceView.as_view(), name='attendance'),
    path('mark_attendance/', AttendanceAPIVIew.as_view(), name='mark-attendance')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)