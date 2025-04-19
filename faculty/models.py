

# student/models.py


from django.db import models
from custom_admin.models import *
from django.contrib.auth.models import User

class Internship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.company}"




class PlacementApplication(models.Model):
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    next_round_date = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('interview', 'Interview Scheduled'),
        ('next_round', 'Next Round Scheduled'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),

    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    round_updates = models.TextField(blank=True, null=True) # added round_updates
    shortlisted = models.BooleanField(default=False) # Add shortlisted field



    def __str__(self):
        return f"{self.student.student_id} - {self.placement.company}"


