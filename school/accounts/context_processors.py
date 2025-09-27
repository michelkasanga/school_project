from students.models import Students

def student_context(request):
    student = None
    if request.user.is_authenticated:
        try:
            student = Students.objects.get(user = request.user)
        except Students.DoesNotExist:
            student = None
    return{ 'current_student':student }