from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

# Models are imported correctly
from .models import Student, Faculty, Event, Placement

from django.contrib.auth.models import User
def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/custom_admin_dashboard/')
        else:
            messages.error(request, "Invalid credentials or not an admin user.")

    return render(request, 'homepage.html')


def admin_login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            return render(request, 'custom_admin/login.html')

        user = authenticate(request, username=user.username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('custom_admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'custom_admin/login.html')

    return render(request, 'custom_admin/login.html')

@login_required(login_url='/login/')
def custom_admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'custom_admin/dashboard.html')

@login_required(login_url='/login/')
def add_manage_students(request):
    return render(request, 'custom_admin/students.html')

@login_required(login_url='/login/')
def add_student(request):

    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        full_name = request.POST.get('full_name', '').strip()
        # email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        department = request.POST.get('department', '')
        batch = request.POST.get('batch', '')
        username = request.POST.get('username', '').strip()
        password = 'STUDENT'
        today_date = datetime.today().date()
        chatId = f'{username}-{today_date}'
        print('Student Chat Id', chatId)

        if not all([full_name, email, phone, department, batch, username]):
            messages.error(request, "All fields are required.")
            return redirect('custom_admin:manage_students')

        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with that username already exists.")
            return redirect('custom_admin:manage_students')
        
        if Student.objects.filter(email=email).exists():  
            messages.error(request, "Student email already exists.")
            return redirect('custom_admin:manage_students')


        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            Student.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                department=department,
                batch=batch,
                studentChatId=chatId
            )

            messages.success(request, "Student added successfully!")
            return redirect('custom_admin:manage_students')

        except IntegrityError:
            messages.error(request, "A user with that email already exists.")
            return redirect('custom_admin:manage_students')

    return redirect('custom_admin:manage_students')

@login_required(login_url='/login/')
def manage_students(request):
    students = Student.objects.all()

    search_query = request.GET.get('search', '').strip()
    department_filter = request.GET.get('department', '')
    batch_filter = request.GET.get('batch', '')
    is_approved = request.GET.get('is_approved', '')

    if search_query:
        students = students.filter(Q(full_name__icontains=search_query) | Q(email__icontains=search_query))

    if department_filter:
        students = students.filter(department=department_filter)

    if batch_filter:
        students = students.filter(batch=batch_filter)

    if is_approved:
        students = students.filter(is_approved=is_approved == "true")  # Fixed boolean comparison

    return render(request, "custom_admin/students.html", {"students": students})

@login_required(login_url='/login/')
def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == "POST":
        student.full_name = request.POST.get("full_name", "").strip()
        student.email = request.POST.get("email", "").strip().lower()
        student.phone = request.POST.get("phone", "").strip()
        student.department = request.POST.get("department", "")
        student.batch = request.POST.get("batch", "")
        student.is_approved = request.POST.get("is_approved", "off") == "on"
        student.save()
        messages.success(request, "Student updated successfully!")
        return redirect(reverse('custom_admin:manage_students') + '?action=manage')

    context = {'student': student, 'students': Student.objects.all()}
    return render(request, 'custom_admin/students.html', context)

@login_required(login_url='/login/')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    student.delete()
    user.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('custom_admin:manage_students') + '?action=manage')

@login_required(login_url='/login/')
def add_manage_faculties(request):
    return render(request, 'custom_admin/faculty.html')

@login_required(login_url='/login/')
def add_faculty(request):

    if request.method == 'POST':
        email = request.POST.get('email').strip().lower() 
        full_name = request.POST.get('full_name', '').strip()
        # email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        department = request.POST.get('department', '')
        subject = request.POST.get('subject', '')
        username = request.POST.get('username', '').strip()
        password = 'FACULTY'
        today_date = datetime.today().date()
        chatId = f'{username}-{today_date}'
        print('Faculty Chat Id', chatId)
        print('Submitted email:', email)
        print('Existing emails in User:', list(User.objects.values_list('email', flat=True)))

        if not all([full_name, email, phone, department, username]):
            messages.error(request, "All fields are required.")
            return redirect('custom_admin:manage_faculty')

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('custom_admin:manage_faculty')

        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with this username already exists.")
            return redirect('custom_admin:manage_faculty')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            Faculty.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                department=department,
                subject=subject,
                facultyChatId=chatId
            )

            messages.success(request, "Faculty added successfully!")
            return redirect('custom_admin:manage_faculty')

        except IntegrityError:
            messages.error(request, "An error occurred. Please try again.")
            return redirect('custom_admin:manage_faculty')

    return redirect('custom_admin:manage_faculty')

@login_required(login_url='/login/')
def manage_faculty(request):
    faculty_list = Faculty.objects.all()

    search_query = request.GET.get('search', '').strip()
    department_filter = request.GET.get('department', '')
    subject_filter = request.GET.get('subject', '')
    is_approved = request.GET.get('is_approved', '')

    if search_query:
        faculty_list = faculty_list.filter(Q(full_name__icontains=search_query) | Q(email__icontains=search_query))

    if department_filter:
        faculty_list = faculty_list.filter(department=department_filter)

    if subject_filter:
        faculty_list = faculty_list.filter(subject__icontains=subject_filter)  # Fixed to use __icontains

    if is_approved:
        faculty_list = faculty_list.filter(is_approved=is_approved == "true")  # Fixed boolean comparison

    return render(request, "custom_admin/faculty.html", {"faculty_list": faculty_list})

@login_required(login_url='/login/')
def edit_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)

    if request.method == "POST":
        faculty.full_name = request.POST.get("full_name", "").strip()
        faculty.email = request.POST.get("email", "").strip().lower()
        faculty.phone = request.POST.get("phone", "").strip()
        faculty.department = request.POST.get("department", "")
        faculty.subject = request.POST.get("subject", "")
        faculty.is_approved = request.POST.get("is_approved", "off") == "on"
        faculty.save()
        messages.success(request, "Faculty updated successfully!")
        return redirect(reverse('custom_admin:manage_faculty') + '?action=manage')

    context = {'faculty': faculty, 'faculty_list': Faculty.objects.all()}
    return render(request, 'custom_admin/faculty.html', context)

@login_required(login_url='/login/')
def delete_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    user = faculty.user
    faculty.delete()
    user.delete()
    messages.success(request, f'Faculty "{faculty.full_name}" deleted successfully.')
    return redirect('custom_admin:manage_faculty')

@login_required(login_url='/login/')
def add_manage_event(request):
    return render(request, 'custom_admin/events.html')

@login_required(login_url='/login/')
def manage_events(request):
    event_list = Event.objects.all()

    search_query = request.GET.get('search', '').strip()
    filter_date = request.GET.get('filter_date', '')

    if search_query:
        event_list = event_list.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if filter_date == "upcoming":
        event_list = event_list.filter(start_date__gte=timezone.now().date())
    elif filter_date == "past":
        event_list = event_list.filter(start_date__lt=timezone.now().date())

    return render(request, "custom_admin/events.html", {"event_list": event_list})

@login_required(login_url='/login/')
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        venue = request.POST.get('venue', '').strip()

        if not all([title, start_date, venue]):
            messages.error(request, "Title, start date, and venue are required.")
            return redirect('custom_admin:manage_events')

        if Event.objects.filter(title=title, start_date=start_date).exists():
            messages.error(request, "An event with this title and start date already exists.")
            return redirect('custom_admin:manage_events')

        Event.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            venue=venue,
        )
        messages.success(request, "Event added successfully!")
        return redirect('custom_admin:manage_events')

    return redirect('custom_admin:manage_events')

@login_required(login_url='/login/')
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        event.title = request.POST.get("title", "").strip()
        event.description = request.POST.get("description", "").strip()
        event.start_date = request.POST.get("start_date", "")
        event.end_date = request.POST.get("end_date", "")
        event.venue = request.POST.get("venue", "").strip()
        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect(reverse('custom_admin:manage_events') + '?action=manage')

    context = {'event': event, 'event_list': Event.objects.all()}
    return render(request, 'custom_admin/events.html', context)

def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'GET':
        event.delete()
        messages.success(request, f'Event "{event.title}" deleted successfully.')
        return redirect('custom_admin:manage_events')
    return redirect('custom_admin:manage_events')

@login_required(login_url='/login/')
def add_manage_placements(request):
    return render(request, 'custom_admin/placements.html')

@login_required(login_url='/login/')
def add_placement(request):
    if request.method == 'POST':
        company = request.POST.get("company", "").strip()
        job_title = request.POST.get("role", "").strip()
        package = request.POST.get("package", "").strip()
        location = request.POST.get("location", "").strip()
        application_deadline = request.POST.get("close_date", "")

        if not all([company, job_title, package, location]):
            messages.error(request, "All fields are required.")
            return redirect('custom_admin:manage_placement')

        try:
            package = float(package)
            Placement.objects.create(
                company=company,
                job_title=job_title,
                package=package,
                location=location,
                application_deadline=application_deadline if application_deadline else None,
            )
            messages.success(request, "Placement added successfully!")
        except ValueError:
            messages.error(request, "Package must be a number.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect(reverse("custom_admin:manage_placement") + "?action=manage")

    return render(request, "custom_admin/placements.html")

@login_required(login_url='/login/')
def manage_placement(request):
    search_query = request.GET.get("search", "").strip()
    filter_by_role = request.GET.get("role", "").strip()
    filter_by_location = request.GET.get("location", "").strip()

    companies = Placement.objects.all()

    if search_query:
        companies = companies.filter(
            Q(company__icontains=search_query) |
            Q(job_title__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    if filter_by_role:
        companies = companies.filter(job_title__icontains=filter_by_role)

    if filter_by_location:
        companies = companies.filter(location__icontains=filter_by_location)

    return render(request, 'custom_admin/placements.html', {
        'companies': companies,
        'search_query': search_query,
        'filter_by_role': filter_by_role,
        'filter_by_location': filter_by_location,
    })

@login_required(login_url='/login/')
def edit_placement(request, placement_id):
    placement = get_object_or_404(Placement, id=placement_id)

    if request.method == "POST":
        company = request.POST.get("company", "").strip()
        job_title = request.POST.get("role", "").strip()
        package = request.POST.get("package", "").strip()
        location = request.POST.get("location", "").strip()
        application_deadline = request.POST.get("close_date", "") or None

        if not all([company, job_title, package, location]):
            messages.error(request, "All fields are required.")
            return redirect(reverse("custom_admin:manage_placement") + "?action=manage")

        try:
            package = float(package)
            placement.company = company
            placement.job_title = job_title
            placement.package = package
            placement.location = location
            placement.application_deadline = application_deadline
            placement.save()
            messages.success(request, "Placement updated successfully!")
        except ValueError:
            messages.error(request, "Package must be a number.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect(reverse("custom_admin:manage_placement") + "?action=manage")

    return render(request, "custom_admin/placements.html", {"placement": placement})

@login_required(login_url='/login/')
def delete_placement(request, placement_id):
    placement = get_object_or_404(Placement, pk=placement_id)
    if request.method == 'GET':
        placement.delete()
        messages.success(request, f'Placement "{placement.company}" deleted successfully.')
        return redirect(reverse("custom_admin:manage_placement") + "?action=manage")
    return redirect('custom_admin:manage_placement')

@login_required(login_url='/login/')
def logout_admin(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect(reverse('login'))

from django.shortcuts import render, redirect
from django.urls import reverse

def catch_all(request, path):
    if path.startswith('faculty/'):
        return redirect(reverse('faculty:faculty_login') + f'?next=/{path}')
    elif path.startswith('student/'):
        return redirect(reverse('student:student_login') + f'?next=/{path}')
    elif path.startswith('custom_admin/'):
        return redirect(reverse('custom_admin:login') + f'?next=/{path}')
    else:
        return redirect('home')