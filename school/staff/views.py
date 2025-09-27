from django.shortcuts import render, get_object_or_404
from .models import Staff, Dean
from general.models import *
from django.core.paginator import Paginator



def dean(request):

    # Filtrage par option si paramètre GET
    option_id = request.GET.get('option')
    queryset = Dean.objects.select_related('staff', 'option')
    if option_id:
        queryset = queryset.filter(option_id=option_id)

    # Grouper les doyens par option
    from collections import OrderedDict
    options_dict = OrderedDict()
    for dean in queryset:
        option = dean.option
        if option not in options_dict:
            options_dict[option] = []
        options_dict[option].append(dean.staff)

    context = {
        'options': options_dict,
    }
    return render(request, 'home/dean.html', context)


def staff(request):
    staff = Staff.objects.only('id', 'name', 'surname', 'firstname', 'title', 'role')
    paginator = Paginator(staff,10 )
    
    page_number = request.GET.get("page")
    staffs = paginator.get_page(page_number)
    
    context = {
       'staffs':staffs,
       'titre':"Staff",
    }
    
    return render(request, 'home/staff.html', context)
