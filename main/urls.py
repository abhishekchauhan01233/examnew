from django.urls import path
from . import views
from stest import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('exampattern/', views.exampattern, name='exampattern'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('dates/', views.dates, name='dates'),
    path('syllabus/', views.syllabus, name='syllabus'),
    path('scholarships/', views.scholarships, name='scholarships'),
    path('studentregister/', views.studentregister, name='student_register'),
    path('studentlogin/', views.studentlogin, name='student_login'),
    path('student/', views.student, name='student'),
    path('profile/', views.profile, name='profile'),
    path('taketest/', views.take_test, name='taketest'),
    path('result/', views.result, name='result'),
    path('feedback/', views.feedback, name='feedback'),
    path('test/', views.test, name='test'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)