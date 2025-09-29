from django.http import JsonResponse
from .models import Fees
from students.models import Students

def get_fees_for_student(request):
    student_id = request.GET.get('student_id')
    try:
        student = Students.objects.get(pk=student_id)
        fees = Fees.objects.filter(section=student.section, classe=student.classe)
        data = [
            {'id': fee.id, 'name': fee.name, 'amount': float(fee.amount)}
            for fee in fees
        ]
        return JsonResponse({'fees': data})
    except Students.DoesNotExist:
        return JsonResponse({'fees': []})
