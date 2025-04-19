# from faculty.models import Faculty  # Import your Faculty model
from custom_admin.models import *
def student_context(request):
    if request.user.is_authenticated:
        student = Student.objects.filter(email=request.user.email).first()
        return {'student':student}  # This will be available globally in all templates
    return {}
