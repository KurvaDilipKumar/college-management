from django.contrib import admin
from .models import (
    Student, Faculty, Marks, Attendance,
    Event, Placement
)

# -------------------- STUDENT --------------------
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'email', 'department', 'batch', 'is_approved')
    search_fields = ('student_id', 'full_name', 'email', 'phone')
    list_filter = ('batch', 'department')
    ordering = ('full_name',)
    list_per_page = 10

admin.site.register(Student, StudentAdmin)


# -------------------- MARKS --------------------
@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_full_name', 'subject', 'marks', 'exam_type', 'semester', 'mid_term')
    list_filter = ('exam_type', 'semester', 'student__department', 'student__batch')
    search_fields = ('student__student_id', 'student__full_name', 'subject')

    def get_full_name(self, obj):
        return obj.student.full_name
    get_full_name.short_description = 'Student Name'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = db_field.remote_field.model.objects.all().order_by('student_id')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# -------------------- ATTENDANCE --------------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present', 'event_attended', 'seminar_attended')
    list_filter = ('date', 'student__batch', 'student__department', 'is_present', 'event_attended', 'seminar_attended')
    search_fields = ('student__student_id', 'student__full_name')


# -------------------- FACULTY --------------------
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'full_name', 'email', 'phone', 'department', 'subject', 'designation')
    list_display_links = ('faculty_id', 'full_name')
    search_fields = ('faculty_id', 'full_name', 'email', 'phone')
    list_filter = ('department', 'subject')
    ordering = ('full_name',)
    list_per_page = 10

admin.site.register(Faculty, FacultyAdmin)


# -------------------- EVENT --------------------
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'venue')
    search_fields = ('title', 'venue')
    list_filter = ('start_date', 'end_date')
    ordering = ('-created_at',)

admin.site.register(Event, EventAdmin)


# -------------------- PLACEMENT --------------------
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('company', 'job_title', 'package', 'location', 'application_deadline', 'created_at')
    search_fields = ('company', 'job_title')
    list_filter = ('application_deadline',)

admin.site.register(Placement, PlacementAdmin)
