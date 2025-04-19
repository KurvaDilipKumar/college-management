# from faculty.models import Faculty  # Import your Faculty model
from custom_admin.models import *
def faculty_context(request):
    if request.user.is_authenticated:
        faculty = Faculty.objects.filter(email=request.user.email).first()
        return {'faculty': faculty}  # This will be available globally in all templates
    return {}
