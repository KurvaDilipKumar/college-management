from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PlacementApplication

class PlacementApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'placement', 'application_date', 'status', 'interview_date', 'next_round_date')
    search_fields = ('student__student_id', 'placement__company', 'status')
    list_filter = ('status', 'application_date', 'placement')

admin.site.register(PlacementApplication, PlacementApplicationAdmin)