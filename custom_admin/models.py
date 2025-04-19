from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# ======================
# STUDENT MODEL
# ======================

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('AIDS', 'Artificial Intelligence and Data Science'),
        ('CIVIL', 'Civil Engineering'),
        ('MECH', 'Mechanical Engineering'),
    ]
    BATCH_CHOICES = [
        ('R21', '2021'),
        ('R22', '2022'),
        ('R23', '2023'),
        ('R24', '2024'),
        ('R25', '2025'),
    ]

    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    batch = models.CharField(max_length=50, choices=BATCH_CHOICES)

    student_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    is_approved = models.BooleanField(default=False)

    tenth_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    inter_diploma_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    btech_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    native_address = models.TextField(null=True, blank=True)
    hostel_day_scholar = models.CharField(max_length=20, null=True, blank=True)

    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    tenth_marks_photo = models.ImageField(upload_to='tenth_marks/', null=True, blank=True)
    inter_diploma_certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
    studentChatId = models.CharField(null=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student = Student.objects.filter(batch=self.batch, department=self.department).order_by('-id').first()
            if last_student and last_student.student_id:
                last_number = int(last_student.student_id[-2:])
                new_number = f"{last_number + 1:02d}"
            else:
                new_number = "01"
            self.student_id = f"{self.batch}{self.department}{new_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


# ======================
# MARKS MODEL
# ======================

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    exam_type = models.CharField(max_length=10, choices=[('sem', 'Semester'), ('mid', 'Mid-Term')])
    semester = models.IntegerField()
    mid_term = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject} - {self.marks} - {self.exam_type} - Sem {self.semester} - Mid {self.mid_term}"

    class Meta:
        verbose_name_plural = "Marks"


# ======================
# ATTENDANCE MODEL
# ======================

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    event_attended = models.BooleanField(default=False)
    seminar_attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.student_id} - {self.date}"


# ======================
# FACULTY MODEL
# ======================

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()  
    phone = models.CharField(max_length=15)

    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('AIDS', 'Artificial Intelligence and Data Science'),
        ('CIVIL', 'Civil Engineering'),
        ('MECH', 'Mechanical Engineering'),
    ]

    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    subject = models.TextField(blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    areas_of_interest = models.TextField(blank=True, null=True)

    tenth_marks = models.CharField(max_length=5, null=True, blank=True)
    inter_diploma_marks = models.CharField(max_length=5, null=True, blank=True)
    degree_marks = models.CharField(max_length=5, null=True, blank=True)
    professional_degree = models.CharField(max_length=100, blank=True, null=True)

    experience = models.TextField(blank=True, null=True)
    previous_colleges = models.TextField(null=True, blank=True)

    research_activities = models.TextField(blank=True, null=True)
    awards = models.TextField(blank=True, null=True)
    events_organized = models.TextField(blank=True, null=True)
    admin_positions = models.TextField(blank=True, null=True)

    photo = models.ImageField(upload_to='faculty_photos/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    facultyChatId = models.CharField(null=True, max_length=100, blank=True)
    faculty_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.faculty_id:
            last_faculty = Faculty.objects.filter(department=self.department).order_by('-id').first()
            if last_faculty and last_faculty.faculty_id:
                last_number = int(last_faculty.faculty_id[-2:])
                new_number = f"{last_number + 1:02d}"
            else:
                new_number = "01"
            self.faculty_id = f"{self.department}{new_number}"

        if not self.slug and self.full_name:
            base_slug = slugify(f"{self.full_name}-{self.faculty_id}")
            slug = base_slug
            counter = 1
            while Faculty.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.faculty_id})"

    class Meta:
        verbose_name_plural = "Faculties"


# ======================
# EVENT MODEL
# ======================

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    venue = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# ======================
# PLACEMENT MODEL
# ======================

class Placement(models.Model):
    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    package = models.FloatField(help_text="Salary in LPA")
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField(null=True, blank=True, help_text="Placement closing date")
    round_updates = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company} - {self.job_title}"