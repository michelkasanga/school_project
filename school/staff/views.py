from django.shortcuts import render
from .models import Staff, Dean
from django.core.paginator import Paginator



def dean(request):
    data ={}
    for dean in Dean.objects.select_related("staff"):
        if dean.option not in data:
            data[dean.option] = []
        data[dean.option].append(str(dean.staff))
    
    context = {
        'options' :data,
        'dean': Dean.objects.select_related('option')
       
    }
    
    return render(request, 'home/dean.html', context)


def staff(request):
    staff = Staff.objects.all()
    paginator = Paginator(staff,10 )
    
    page_number = request.GET.get("page")
    staffs = paginator.get_page(page_number)
    
    context = {
       'staffs':staffs,
       'titre':"Staff"
    }
    
    return render(request, 'home/staff.html', context)
