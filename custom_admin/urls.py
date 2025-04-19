from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'custom_admin'  # Add this line

urlpatterns = [
    path('logout_admin/', logout_admin, name='logout_admin'),
    path('custom_admin_dashboard', custom_admin_dashboard, name='custom_admin_dashboard'),
    path('add_manage_students', add_manage_students, name='add_manage_students'),
    path('add_student/', add_student, name='add_student'),
    path("manage_students/", manage_students, name="manage_students"),
    path('students/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', delete_student, name='delete_student'),

    path('add_manage_faculties', add_manage_faculties, name='add_manage_faculties'),
    path('add_faculty', add_faculty, name='add_faculty'),
    path('manage_faculty', manage_faculty, name='manage_faculty'),
    path('faculty/edit/<int:faculty_id>/',edit_faculty, name='edit_faculty'),
    path('faculties/delete/<int:faculty_id>/',delete_faculty, name='delete_faculty'), # Corrected URL

    path('add_manage_event', add_manage_event, name='add_manage_event'),
    path('add_event/', add_event, name='add_event'),
    path('manage_events/', manage_events, name='manage_events'),
    path('edit_event/<int:event_id>/', edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),  # Corrected URL

    path('add_manage_placements', add_manage_placements, name='add_manage_placements'),
    path("add_placement/", add_placement, name="add_placement"),
    path("manage_placement/", manage_placement, name="manage_placement"),
    path("placements/edit/<int:placement_id>/", edit_placement, name="edit_placement"),
    path('placements/delete/<int:placement_id>/',delete_placement, name='delete_placement'),
]