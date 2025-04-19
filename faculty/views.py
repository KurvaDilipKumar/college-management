from django.contrib.auth import authenticate, login, logout

from custom_admin.models import *

import datetime

from django.contrib.auth import authenticate, login

from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from custom_admin.models import *
from chatting.models import *
from custom_admin.models import *







from django.shortcuts import render, get_object_or_404
from .models import Faculty

def faculty_list(request):
    faculties = Faculty.objects.filter(is_approved=True)
    return render(request, 'faculty/faculty_list.html', {'faculties': faculties})

def faculty_detail(request, slug):
    faculty = get_object_or_404(Faculty, slug=slug)
    return render(request, 'faculty/faculty_detail.html', {'faculty': faculty})


def Faculty_login_page(request):
    request.session.flush()  # Clear session to avoid conflicts
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        request.session['facultyEmail'] = email

        try:
            faculty = Faculty.objects.get(email=email)
            print(f"Faculty: {faculty.email}, User: {faculty.user}, Username: {faculty.user.username if faculty.user else None}")
        except Faculty.DoesNotExist:
            messages.error(request, "Invalid email.")
            return render(request, 'faculty/login.html')

        if not faculty.user:
            messages.error(request, "No user account linked to this faculty.")
            return render(request, 'faculty/login.html')

        if faculty.is_approved:
            user = authenticate(request, username=faculty.user.username, password=password)
            if user is None:
                
                user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                print(f"Logged in user: {user}, User email: {user.email}")
                return redirect('faculty:faculty_dashboard')
            else:
                messages.error(request, "Password incorrect")
        else:
            messages.error(request, "Faculty approval pending.")

    return render(request, 'faculty/login.html')



@login_required(login_url='/faculty_login/')
def Faculty_dashboard(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
        print(f"Dashboard Faculty: {faculty.email}, Approved: {faculty.is_approved}")
    except Faculty.DoesNotExist:
        print(f"No faculty found for user: {request.user.username}")
        return redirect('faculty_login')

    if not faculty.is_approved:
        return redirect('faculty_login')

    # Split the subject field into a list before passing to the template
    faculty.subject_list = split_field(faculty.subject)

    return render(request, 'faculty/dashboard.html', {'faculty': faculty})


@login_required(login_url='/faculty_login/')
def faculty_logout(request):
    logout(request)
    messages.success(request, "Faculty Logout Successful.")
    return redirect('faculty:faculty_login')



@login_required(login_url='/faculty_login/')
def Faculty_profile(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, "Faculty profile not found.")
        return redirect('faculty:faculty_dashboard')

    return render(request, 'faculty/profile.html', {'faculty': faculty})


@login_required(login_url='/faculty_login/')
def student_details(request):
    students = Student.objects.all()

    search_query = request.GET.get('search')
    department_filter = request.GET.get('department')
    batch_filter = request.GET.get('batch')

    if search_query:
        students = students.filter(full_name__icontains=search_query)

    if department_filter:
        students = students.filter(department=department_filter)

    if batch_filter:
        students = students.filter(batch=batch_filter)

    return render(request, 'faculty/student_details.html', {'students': students})


@login_required(login_url='/faculty_login/')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.full_name = request.POST.get('full_name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.department = request.POST.get('department')
        student.batch = request.POST.get('batch')

        tenth_marks = request.POST.get('tenth_marks')
        inter_diploma_marks = request.POST.get('inter_diploma_marks')
        btech_marks = request.POST.get('btech_marks')

        student.tenth_marks = float(tenth_marks) if tenth_marks else None
        student.inter_diploma_marks = float(inter_diploma_marks) if inter_diploma_marks else None
        student.btech_marks = float(btech_marks) if btech_marks else None

        student.native_address = request.POST.get('native_address')
        student.hostel_day_scholar = request.POST.get('hostel_day_scholar')

        student.save()
        messages.success(request, "Student details updated successfully.")
        return redirect('faculty:student_details')  # Corrected redirect

    return render(request, 'faculty/student_details.html', {'student': student})

@login_required(login_url='/faculty_login/')
def add_marks(request):
    student_model = Student
    try:
        faculty_details = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, "Faculty not found.")
        return redirect('faculty:faculty_dashboard')
    fSubject = faculty_details.subject

    batches = student_model.BATCH_CHOICES
    departments = student_model.DEPARTMENT_CHOICES

    if request.method == "POST":
        student_id = request.POST.get('student_id')
        batch = request.POST.get('batch')
        department = request.POST.get('department')
        subject = request.POST.get('subject')
        marks = request.POST.get('marks')
        exam_type = request.POST.get('exam_type')
        semester = request.POST.get('semester')
        mid_term = request.POST.get('mid_term')

        try:
            student = Student.objects.get(student_id=student_id, batch=batch, department=department)
        except Student.DoesNotExist:
            messages.error(request, "Student not found.")
            return redirect('faculty:add_marks')

        if exam_type == 'mid':
            Marks.objects.create(student=student, subject=subject, marks=marks, exam_type=exam_type, semester=semester, mid_term=mid_term)
        else:
            Marks.objects.create(student=student, subject=subject, marks=marks, exam_type=exam_type, semester=semester, mid_term=None)
        messages.success(request, "Marks added successfully.")

        return redirect('faculty:manage_marks')

    context = {
        'batches': [b[0] for b in batches],
        'departments': departments,
        'fSubject': fSubject,
    }

    return render(request, 'faculty/marks.html', context)



@login_required(login_url='/faculty_login/')
def manage_marks(request):
    try:
        faculty_details = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, "Faculty not found.")
        return redirect('faculty:faculty_dashboard')
    faculty_subject = faculty_details.subject
    marks_list = Marks.objects.filter(subject=faculty_subject)

    search_query = request.GET.get('search')
    filter_subject = request.GET.get('filter_subject')

    if search_query:
        marks_list = marks_list.filter(student__student_id__icontains=search_query)

    if filter_subject:
        marks_list = marks_list.filter(subject__icontains=filter_subject)

    context = {
        'marks_list': marks_list,
    }

    return render(request, 'faculty/marks.html', context)



@login_required(login_url='/faculty_login/')
def edit_marks(request, marks_id):
    marks_instance = get_object_or_404(Marks, id=marks_id)
    student_model = Student
    batches = student_model.BATCH_CHOICES
    departments = student_model.DEPARTMENT_CHOICES

    if request.method == "POST":
        student_id = request.POST.get('student_id')
        batch = request.POST.get('batch')
        department = request.POST.get('department')
        subject = request.POST.get('subject')
        marks = request.POST.get('marks')
        exam_type = request.POST.get('exam_type')
        semester = request.POST.get('semester')
        mid_term = request.POST.get('mid_term')

        try:
            student = Student.objects.get(student_id=student_id, batch=batch, department=department)
        except Student.DoesNotExist:
            messages.error(request, "Student not found.")
            return redirect('edit_marks', marks_id=marks_id)

        marks_instance.student = student
        marks_instance.subject = subject
        marks_instance.marks = marks
        marks_instance.exam_type = exam_type
        marks_instance.semester = semester
        if exam_type == 'mid':
            marks_instance.mid_term = mid_term
        else:
            marks_instance.mid_term = None
        marks_instance.save()
        messages.success(request, "Marks updated successfully.")
        return redirect('faculty:manage_marks')

    context = {
        'marks_instance': marks_instance,
        'batches': [b[0] for b in batches],
        'departments': departments,
    }

    return render(request, 'faculty/marks.html', context)



@login_required(login_url='/faculty_login/')
def attendance(request):
    batches = [b[0] for b in Student.BATCH_CHOICES]
    departments = Student.DEPARTMENT_CHOICES
    students = []
    attendance_records = {}
    attendance_date = date.today()

    if request.method == "POST":
        department = request.POST.get('department')
        batch = request.POST.get('batch')
        date_str = request.POST.get('date')

        if date_str:
            try:
                attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format.")
                return redirect(request.path)

        students = Student.objects.filter(department=department, batch=batch)

        if not students.exists():
            messages.error(request, "No students found for the selected batch and department.")
            return redirect(request.path)

        for student in students:
            is_present = request.POST.get(f'attendance_{student.id}') == "on"
            event_attended = request.POST.get(f'event_{student.id}') == "on"
            seminar_attended = request.POST.get(f'seminar_{student.id}') == "on"

            attendance_record, created = Attendance.objects.get_or_create(student=student, date=attendance_date)
            attendance_record.is_present = is_present
            attendance_record.event_attended = event_attended
            attendance_record.seminar_attended = seminar_attended
            attendance_record.save()

        messages.success(request, "Attendance saved successfully.")
        return redirect(f"{request.path}?date={attendance_date}&department={department}&batch={batch}")

    elif request.method == "GET":
        department = request.GET.get('department')
        batch = request.GET.get('batch')
        date_str = request.GET.get('date')

        if date_str:
            try:
                attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format.")
                return redirect(request.path)

        if department and batch:
            students = Student.objects.filter(department=department, batch=batch)
            attendance_records = {
                att.student.id: att for att in Attendance.objects.filter(date=attendance_date, student__in=students)
            }

    for student in students:
        attendance_record = attendance_records.get(student.id)
        student.is_present = attendance_record.is_present if attendance_record else False
        student.event_attended = attendance_record.event_attended if attendance_record else False
        student.seminar_attended = attendance_record.seminar_attended if attendance_record else False

    context = {
        'batches': batches,
        'departments': departments,
        'students': students,
    }

    return render(request, 'faculty/attendance.html', context)


@login_required(login_url='/faculty_login/')
def add_professional_details(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
        print(faculty)
    except Faculty.DoesNotExist:
        faculty = None

    if request.method == "POST":
        if faculty:
            faculty.tenth_marks = request.POST.get('tenth_marks')
            faculty.inter_diploma_marks = request.POST.get('inter_diploma_marks')
            faculty.degree_marks = request.POST.get('degree_marks')
            faculty.professional_degree = request.POST.get('professional_degree')
            faculty.experience = request.POST.get('experience')
            previous_colleges = []
            for key, value in request.POST.items():
                if key.startswith('previous_colleges_'):
                    previous_colleges.append(value)

            faculty.previous_colleges = ','.join(previous_colleges)
            faculty.save()
            messages.success(request, "Professional details updated successfully.")
            return redirect('faculty:add_professional_details')

    context = {
        'faculty': faculty,
        'previous_colleges_list': [college.strip() for college in faculty.previous_colleges.split(',')] if faculty and faculty.previous_colleges else []
    }
    return render(request, 'faculty/add_professional_details.html', context)



@login_required(login_url='/faculty_login/')
def add_student_internship(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        company = request.POST.get('company')
        duration = request.POST.get('duration')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except ValueError:
            messages.error(request, "Invalid date format. Please useсибо-MM-DD.")
            return redirect('faculty:add_student_internship')

        try:
            student = Student.objects.get(student_id=student_id)
            Internship.objects.create(student=student, company=company, duration=duration, start_date=start_date, end_date=end_date)
            messages.success(request, "Internship added successfully.")
            return redirect('faculty:manage_student_internships')
        except Student.DoesNotExist:
            messages.error(request, f"Student with ID {student_id} does not exist.")
            return redirect('faculty:add_student_internship')

    return render(request, 'faculty/student_internship.html')

@login_required(login_url='/faculty_login/')
def edit_student_internship(request, internship_id):
    internship = Internship.objects.get(id=internship_id)
    if request.method == 'POST':
        internship.company = request.POST.get('company')
        internship.duration = request.POST.get('duration')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        try:
            internship.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            internship.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except ValueError:
            messages.error(request, "Invalid date format. Please useсибо-MM-DD.")
            return redirect('faculty:edit_student_internship', internship_id=internship_id)

        internship.save()
        messages.success(request, "Internship updated successfully.")
        return redirect('faculty:manage_student_internships')
    return render(request, 'faculty/student_internship.html', {'internship': internship})

@login_required(login_url='/faculty_login/')
def manage_student_internships(request):
    search_term = request.GET.get('search', '')
    if search_term:
        internships = Internship.objects.filter(student__student_id__icontains=search_term)
    else:
        internships = Internship.objects.all()
    return render(request, 'faculty/student_internship.html', {'internships': internships})

@login_required(login_url='/faculty_login/')
def delete_student_internship(request, internship_id):
    internship = get_object_or_404(Internship, pk=internship_id)
    if request.method == 'POST':
        internship.delete()
        messages.success(request, "Internship deleted successfully.")
        return redirect('faculty:manage_student_internships')
    return render(request, 'faculty/student_internship.html',{'internship':internship})



@login_required(login_url='/faculty_login/')
def manage_placements(request):
    placements = Placement.objects.all()
    context = {'placements': placements}
    return render(request, 'faculty/placement_management.html', context)

@login_required(login_url='/faculty_login/')
def manage_applications(request, placement_id):
    placement = get_object_or_404(Placement, pk=placement_id)
    applications = PlacementApplication.objects.filter(placement=placement).select_related('student') #removed status filter
    print(applications)
    context = {'placement': placement, 'applications': applications}
    return render(request, 'faculty/placement_management.html', context)
@login_required(login_url='/faculty_login/')
def update_application(request, application_id):
    application = get_object_or_404(PlacementApplication, pk=application_id)
    if request.method == "POST":
        interview_date_str = request.POST.get('interview_date')
        next_round_date_str = request.POST.get('next_round_date')
        status = request.POST.get('status')

        try:
            interview_date = datetime.fromisoformat(interview_date_str) if interview_date_str else None
            next_round_date = datetime.fromisoformat(next_round_date_str) if next_round_date_str else None
        except ValueError:
            messages.error(request, "Invalid date format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM).")
            return redirect('faculty:update_application', application_id=application_id)

        if status:
            application.interview_date = interview_date
            application.next_round_date = next_round_date
            application.status = status
            application.save()
            messages.success(request, "Application updated successfully.")
            return redirect('faculty:manage_applications', placement_id=application.placement.id)
        else:
            messages.error(request, "Status is required.")
    context = {'application': application}
    return render(request, 'faculty/placement_management.html', context)


@login_required(login_url='/faculty_login/')
def delete_placement(request, placement_id):
    placement = get_object_or_404(Placement, pk=placement_id)
    if request.method == "POST":
        placement.delete()
        messages.success(request, "Placement deleted successfully.")
        return redirect('faculty:manage_placements')
    context = {'placement': placement}
    return render(request, 'faculty/placement_management.html', context)




@login_required(login_url='/faculty_login/')
def add_placement(request):
    if request.method == "POST":
        company = request.POST.get('company')
        job_title = request.POST.get('job_title')
        package = request.POST.get('package')
        location = request.POST.get('location')
        application_deadline = request.POST.get('application_deadline')

        if not package:
            messages.error(request, "Package is required.")
            return render(request, 'faculty/placement_management.html')

        try:
            package = float(package)
        except ValueError:
            messages.error(request, "Package must be a number.")
            return render(request, 'faculty/placement_management.html')

        Placement.objects.create(
            company=company,
            job_title=job_title,
            package=package,
            location=location,
            application_deadline=application_deadline
        )
        messages.success(request, "Placement added successfully.")
        return redirect('faculty:manage_placements')
    return render(request, 'faculty/placement_management.html')

@login_required(login_url='/faculty_login/')
def shortlist_students(request):
    placements = Placement.objects.all()
    applications = None
    if request.method == "POST":
        placement_id = request.POST.get('company')
        placement = get_object_or_404(Placement, pk=placement_id)
        applications = PlacementApplication.objects.filter(placement=placement)
        for application in applications:
            status = request.POST.get(f"status_{application.id}")
            if status:
                application.status = status
                application.save()
        messages.success(request, "Application statuses updated successfully.")
        return redirect('faculty:shortlist_students')
    context = {'placements': placements, 'applications': applications}
    return render(request, 'faculty/placement_management.html', context)





@login_required(login_url='/faculty_login/')
def add_manage_events(request):
    event = None
    event_list = Event.objects.all()

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "add":
            title = request.POST.get('title')
            description = request.POST.get('description')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            venue = request.POST.get('venue')

            if Event.objects.filter(title=title, start_date=start_date).exists():
                messages.error(request, "An event with this title and start date already exists.")
                return redirect('faculty:add_manage_events')

            event = Event.objects.create(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                venue=venue,
            )
            event.save()
            messages.success(request, "Event added successfully!")
            return redirect('faculty:add_manage_events')

        elif action == "edit":
            event_id = request.POST.get('event_id')
            event = get_object_or_404(Event, pk=event_id)

            event.title = request.POST.get("title")
            event.description = request.POST.get("description")
            event.start_date = request.POST.get("start_date")
            event.end_date = request.POST.get("end_date")
            event.venue = request.POST.get("venue")
            event.save()
            messages.success(request, "Event updated successfully!")
            return redirect('faculty:add_manage_events')

        elif action == "delete":
            event_id = request.POST.get('event_id')
            event = get_object_or_404(Event, id=event_id)
            event.delete()
            messages.success(request, "Event deleted successfully!")
            return redirect('faculty:add_manage_events')

    elif request.GET.get('action') == "edit":
        event_id = request.GET.get('event_id')
        event = get_object_or_404(Event, pk=event_id)

    elif request.GET.get('action') == "manage":
        search_query = request.GET.get('search', '').strip()
        filter_date = request.GET.get('filter_date', '')

        if search_query:
            event_list = event_list.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        if filter_date == "upcoming":
            event_list = event_list.filter(start_date__gte=timezone.now().date())
        elif filter_date == "past":
            event_list = event_list.filter(start_date__lt=timezone.now().date())

    context = {
        'event': event,
        'event_list': event_list,
    }
    return render(request, 'faculty/events.html', context)

@login_required(login_url='/faculty_login/')
def manage_events(request):
    event_list = Event.objects.all()

    search_query = request.GET.get('search', '').strip()
    filter_date = request.GET.get('filter_date', '')

    if search_query:
        event_list = event_list.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    if filter_date == "upcoming":
        event_list = event_list.filter(start_date__gte=timezone.now().date())
    elif filter_date == "past":
        event_list = event_list.filter(start_date__lt=timezone.now().date())

    return render(request, "faculty/events.html", {"event_list": event_list})

@login_required(login_url='/faculty_login/')
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        venue = request.POST.get('venue')

        if Event.objects.filter(title=title, start_date=start_date).exists():
            messages.error(request, "An event with this title and start date already exists.")
            return redirect('manage_events')

        events = Event.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            venue=venue,
        )
        events.save()
        messages.success(request, "Event added successfully!")
        return redirect('faculty:manage_events')

    return redirect('faculty:manage_events')

@login_required(login_url='/faculty_login/')
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.start_date = request.POST.get("start_date")
        event.end_date = request.POST.get("end_date")
        event.venue = request.POST.get("venue")
        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect('manage_events')
    context = {
        'event': event,
        'event_list': Event.objects.all(),
    }
    return render(request, 'faculty/events.html', context)

@login_required(login_url='/faculty_login/')
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect('manage_events')



from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
def facultyChatRoom(request):
    if request.method == 'POST':
        email = request.session['facultyEmail']
        if not email:
            return redirect('faculty_login')  # or your login URL

        studentID = request.POST.get('studentId')
        return redirect('faculty:chatRoom', studentID=studentID)
    return render(request, 'faculty/facultyChatRoom.html')


def chatRoom(request, studentID):
    email = request.session['facultyEmail']
    if not email:
        return redirect('faculty_login')
    facultyD = get_object_or_404(Faculty, email=email)
    studentD = get_object_or_404(Student, student_id=studentID)
    studentChatId = studentD.studentChatId
    studentmail = studentD.email
    facultyChatId = facultyD.facultyChatId  # corrected variable name
    conversation = ChattingModel.objects.filter(
        Q(sender_chat_id=studentChatId, receiver_chat_id=facultyChatId) |
        Q(sender_chat_id=facultyChatId, receiver_chat_id=studentChatId)
    ).order_by('timestamp')
    print('sdfdfgfg',conversation)

    if request.method == 'POST':
        text = request.POST.get('text')
        file = request.FILES.get('share_files')
        if text or file:
            chatting = ChattingModel(
                sender_mail=email,
                receiver_mail=studentmail,
                text=text,
                share_files=file,
                sender_chat_id=facultyChatId,
                receiver_chat_id=studentChatId
            )
            chatting.save()
            return redirect('faculty:chatRoom', studentID=studentID)
    return render(request, 'faculty/chatRoom.html', {
        'conversation': conversation,
        'facultyChatId': facultyChatId,
        'studentChatId': studentChatId,
        'studentID': studentID
    })

from django.http import FileResponse
def file_download_view(request, id):
    file_obj = get_object_or_404(ChattingModel, id=id)
    file_path = file_obj.share_files.path
    response = FileResponse(open(file_path, 'rb'))
    return response


from django.shortcuts import render, get_object_or_404
from .models import Faculty

def split_field(field):
    if not field:
        return []
    return [line.strip() for line in field.split('\n') if line.strip()]

def faculty_list(request):
    faculties = Faculty.objects.filter(is_approved=True)
    return render(request, 'faculty/faculty_list.html', {'faculties': faculties})

def faculty_detail(request, slug):
    faculty = get_object_or_404(Faculty, slug=slug)

    faculty.events_list = split_field(faculty.events_organized)
    faculty.subject_list = split_field(faculty.subject)
    faculty.interest_list = split_field(faculty.areas_of_interest)
    faculty.experience_list = split_field(faculty.experience)
    faculty.research_list = split_field(faculty.research_activities)
    faculty.awards_list = split_field(faculty.awards)
    faculty.positions_list = split_field(faculty.admin_positions)

    return render(request, 'faculty/faculty_detail.html', {'faculty': faculty})
