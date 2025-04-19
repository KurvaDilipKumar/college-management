# student/urls.py
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('student_profile/', student_profile, name='student_profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('resume/<int:student_id>/', serve_resume, name='serve_resume'),
    path('certificate/<int:student_id>/', serve_certificate, name='serve_certificate'),
    path('tenth_marks_photo/<int:student_id>/', serve_tenth_marks_photo, name='serve_tenth_marks_photo'),
    path('view_marks/', view_marks, name='view_marks'),
    path('view_attendance/', view_attendance, name='view_attendance'),
    path('view_events/', view_events, name='view_events'),
    path('view_placements/', view_placements, name='view_placements'),
    path('view_internships/', view_internships, name='view_internships'),
    path('placement_management/', placement_management, name='placement_management'),
    path('apply_placement/<int:placement_id>/', apply_placement, name='apply_placement'),
    path('student_logout/', student_logout, name='logout'),
    path('student_login/', student_login, name='student_login'),
    path('placement_management/', placement_management, name='placement_management'),
    path('view_placements/', view_placements, name='view_placements'),
    path('apply_placement/<int:placement_id>/', apply_placement, name='apply_placement'),
    path('studentChatRoom/', studentChatRoom, name='studentChatRoom'),
    path('ChatRoom/<str:facultyId>/', ChatRoom, name='ChatRoom'),
    # path('chatbot/', chatbot, name='chatbot'),
    # path('chat/', chat, name='chat'),
    path('file_download_view/<int:id>/', file_download_view, name='file_download_view')
]