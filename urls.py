from django.urls import path
from .views import *

urlpatterns=[
    path('',home),
    path('register/', regis),
    path('success/', success),
    path('send/', send_mail_regis),
    path('error/', error),
    path('log/', lo),
    path('verify/<auth_token>', verify),
    path('class/', class_view, name='class'),
    path('add-student/', add_student, name='add_student'),
    path('send-message/', send_message, name='send_message'),
    path('student-login/',student_login, name='student_login'),
    path('student-dashboard/',student_dashboard, name='student_dashboard'),
    path('dashboard/',d1),
    path('edit-student/<int:student_id>/',edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/',delete_student, name='delete_student'),
    path('class/',class_view, name='class_view'),
    path('profile/',profile, name='profile'),
    path('raise-doubt/', raise_doubt_view, name='raise_doubt'),
    path('view-doubts/', view_doubts, name='view_doubts'),
    path('upload-assignment/', upload_assignment, name='upload_assignment'),
    path('delete-assignment/<int:assignment_id>/', delete_assignment, name='delete_assignment'),
   ]