from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    path('faculty_login/', views.Faculty_login_page, name='faculty_login'),
    path('faculty_dashboard/', views.Faculty_dashboard, name='faculty_dashboard'),
    path('faculty_profile/', views.Faculty_profile, name='faculty_profile'),
    path('student_details/', views.student_details, name='student_details'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('add_manage_events/', views.add_manage_events, name='add_manage_events'),
    path('add_marks/', views.add_marks, name='add_marks'),
    path('manage_marks/', views.manage_marks, name='manage_marks'),
    path('add_marks/<int:marks_id>/', views.edit_marks, name='edit_marks'),
    path('attendance/', views.attendance, name='attendance'),
    path('add_professional_details/', views.add_professional_details, name='add_professional_details'),
    path('add_student_internship/', views.add_student_internship, name='add_student_internship'),
    path('manage_student_internships/', views.manage_student_internships, name='manage_student_internships'),
    path('edit_student_internship/<int:internship_id>/', views.edit_student_internship, name='edit_student_internship'),
    path('delete_student_internship/<int:internship_id>/', views.delete_student_internship, name='delete_student_internship'),
    path('manage_placements/', views.manage_placements, name='manage_placements'),
    path('manage_applications/<int:placement_id>/', views.manage_applications, name='manage_applications'),
    path('delete_placement/<int:placement_id>/', views.delete_placement, name='delete_placement'),
    path('update_application/<int:application_id>/', views.update_application, name='update_application'),
    path('add_placement/', views.add_placement, name='add_placement'),
    path('shortlist_students/', views.shortlist_students, name='shortlist_students'),
    path('faculty_logout/', views.faculty_logout, name='faculty_logout'),
    path('facultyChatRoom/', views.facultyChatRoom, name='facultyChatRoom'),
    path('chatRoom/<str:studentID>/', views.chatRoom, name='chatRoom'),
    path('file_download_view/<int:id>/', views.file_download_view, name='file_download_view'),

    # Public Faculty List and Detail View (no login needed)
    path('faculties/', views.faculty_list, name='faculty_list'),
    path('faculties/<slug:slug>/', views.faculty_detail, name='faculty_detail'),

] 
