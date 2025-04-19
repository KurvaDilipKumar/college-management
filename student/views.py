from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from custom_admin.models import *
from faculty.models import *
from django.contrib import messages
from django.http import HttpResponseNotFound
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from chatting.models import *
from django.http import FileResponse


@login_required(login_url='/student_login/')
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        if not student.is_approved:
            return redirect('student_login')
        return render(request, 'student/dashboard.html', {'student': student})
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('student_login')

@login_required(login_url='/student_login/')
def student_profile(request):
    student_mail = request.session.get('studentEmail')
    try:
        student = Student.objects.get(email=student_mail)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('student:student_dashboard')
    return render(request, 'student/profile.html', {'student':student})

@login_required(login_url='/student_login/')
def update_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        student.phone = request.POST.get('phone')
        student.native_address = request.POST.get('native_address')
        student.hostel_day_scholar = request.POST.get('hostel_day_scholar')

        if 'resume' in request.FILES:
            student.resume = request.FILES['resume']
        if 'tenth_marks_photo' in request.FILES:
            student.tenth_marks_photo = request.FILES['tenth_marks_photo']
        if 'inter_diploma_certificate' in request.FILES:
            student.inter_diploma_certificate = request.FILES['inter_diploma_certificate']

        def to_decimal(value):
            if value:
                try:
                    return Decimal(value)
                except (ValueError, TypeError):
                    raise ValidationError(f"'{value}' is not a valid decimal number.")
            return None

        try:
            student.tenth_marks = to_decimal(request.POST.get('tenth_marks'))
            student.inter_diploma_marks = to_decimal(request.POST.get('inter_diploma_marks'))
            student.btech_marks = to_decimal(request.POST.get('btech_marks'))
        except ValidationError as e:
            messages.error(request, e)
            return render(request, 'student/update_profile.html', {'student': student})

        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('student:update_profile')

    return render(request, 'student/update_profile.html', {'student': student})

def serve_certificate(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.inter_diploma_certificate:
        file_path = student.inter_diploma_certificate.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    return HttpResponseNotFound("Certificate not found")

def serve_resume(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.resume:
        file_path = student.resume.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    return HttpResponseNotFound("Resume not found")

def serve_tenth_marks_photo(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.tenth_marks_photo:
        file_path = student.tenth_marks_photo.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    return HttpResponseNotFound("10th Mark list not found")

@login_required(login_url='/student_login/')
def view_marks(request):
    student = get_object_or_404(Student, user=request.user)
    marks = Marks.objects.filter(student=student, exam_type='mid').order_by('semester')
    semMarks = Marks.objects.filter(student=student, exam_type='sem')

    semester_filter = request.GET.get('semester')
    if semester_filter:
        marks = marks.filter(semester=semester_filter)

    return render(request, 'student/view_marks.html', {'marks': marks, 'semMarks':semMarks})

@login_required(login_url='/student_login/')
def view_attendance(request):
    student = get_object_or_404(Student, user=request.user)
    attendance = Attendance.objects.filter(student=student).order_by('date')

    event_filter = request.GET.get('event')
    if event_filter:
        if event_filter == 'true':
            attendance = attendance.filter(event_attended=True)
        elif event_filter == 'false':
            attendance = attendance.filter(event_attended=False)

    seminar_filter = request.GET.get('seminar')
    if seminar_filter:
        if seminar_filter == 'true':
            attendance = attendance.filter(seminar_attended=True)
        elif seminar_filter == 'false':
            attendance = attendance.filter(seminar_attended=False)

    date_filter = request.GET.get('date')
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            attendance = attendance.filter(date=date_obj)
        except ValueError:
            pass

    return render(request, 'student/view_attendance.html', {'attendance': attendance})

@login_required(login_url='/student_login/')
def view_events(request):
    events = Event.objects.all().order_by('start_date')

    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    if start_date_filter and end_date_filter:
        try:
            start_date_obj = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            events = events.filter(Q(start_date__lte=end_date_obj) & Q(end_date__gte=start_date_obj))
        except ValueError:
            pass

    return render(request, 'student/view_events.html', {'events': events})

@login_required(login_url='/student_login/')
def view_placements(request):
    student = Student.objects.get(user=request.user)
    deadline_filter = request.GET.get('deadline')

    placements = Placement.objects.all()

    if deadline_filter:
        placements = placements.filter(application_deadline=deadline_filter)

    applied_placements = PlacementApplication.objects.filter(student=student).values_list('placement_id', flat=True)

    context = {
        'placements': placements,
        'applied_placements': applied_placements,
    }
    return render(request, 'student/view_placements.html', context)

@login_required(login_url='/student_login/')
def apply_placement(request, placement_id):
    student = Student.objects.get(user=request.user)
    placement = get_object_or_404(Placement, pk=placement_id)

    if not PlacementApplication.objects.filter(student=student, placement=placement).exists():
        PlacementApplication.objects.create(student=student, placement=placement, application_date=timezone.now())
        return redirect('student:view_placements')
    else:
        messages.error(request, "You have already applied for this placement.")
        return redirect('student:view_placements')

@login_required(login_url='/student_login/')
def view_internships(request):
    student = Student.objects.get(user=request.user)
    internships = Internship.objects.filter(student=student)

    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    if start_date_filter and end_date_filter:
        try:
            start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            internships = internships.filter(start_date__gte=start_date, end_date__lte=end_date)
        except ValueError:
            pass

    return render(request, 'student/view_internships.html', {'internships': internships})

@login_required(login_url='/student_login/')
def placement_management(request):
    try:
        student = Student.objects.get(user=request.user)
        applications = PlacementApplication.objects.filter(student=student).order_by('-application_date')
    except Student.DoesNotExist:
        raise Http404("Student not found.")

    placement_data = []
    for app in applications:
        placement = app.placement
        placement_info = {
            'company': placement.company,
            'job_title': placement.job_title,
            'application_date': app.application_date,
            'status': app.status,
            'round_updates': placement.round_updates,
            'shortlisted': app.shortlisted,
        }
        placement_data.append(placement_info)

    return render(request, 'student/placement_management.html', {'placement_data': placement_data})

def student_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            messages.error(request, "Invalid email.")
            return render(request, 'student/login.html')

        if student.is_approved:
            user = authenticate(request, username=student.user.username, password=password)
            request.session['studentEmail'] = email

            if user is not None:
                login(request, user)
                return redirect('student:student_dashboard')
            else:
                messages.error(request, "Password incorrect")
        else:
            messages.error(request, "Student approval pending.")

    return render(request, 'student/login.html')

def student_logout(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('student_login')

def studentChatRoom(request):
    email = request.session.get('studentEmail')
    student = Student.objects.get(email=email)
    dept = student.department
    facultyList = Faculty.objects.filter(department=dept)
    if request.method == 'POST':
        department = request.POST.get('message_type')
        request.session['faculty_id'] = department
        return redirect('student:ChatRoom', facultyId=department)
    return render(request, 'chatting/selectFaculty.html', {'facultyList':facultyList})

def ChatRoom(request, facultyId):
    facultyDetails = Faculty.objects.get(faculty_id=facultyId)
    facultyChatId = facultyDetails.facultyChatId
    facultymail = facultyDetails.email
    studentmail = request.session.get('studentEmail')
    studentDetails = Student.objects.get(email=studentmail)
    studentChatId = studentDetails.studentChatId

    conversation = ChattingModel.objects.filter(
        Q(sender_chat_id=studentChatId, receiver_chat_id=facultyChatId) |
        Q(sender_chat_id=facultyChatId, receiver_chat_id=studentChatId)
    ).order_by('timestamp')

    if request.method == 'POST':
        text = request.POST.get('text')
        file = request.FILES.get('share_files')
        if text or file:
            chatting = ChattingModel(
                sender_mail=studentmail,
                receiver_mail=facultymail,
                text=text,
                share_files=file,
                sender_chat_id=studentChatId,
                receiver_chat_id=facultyChatId
            )
            chatting.save()
            return redirect('student:ChatRoom', facultyId=facultyId)

    return render(request, 'chatting/facultyStudentChating.html', {
        'conversetion': conversation,
        'facultyId': facultyId,
        'studentChatId': studentChatId
    })

def file_download_view(request, id):
    file_obj = get_object_or_404(ChattingModel, id=id)
    file_path = file_obj.share_files.path
    response = FileResponse(open(file_path, 'rb'))
    return response