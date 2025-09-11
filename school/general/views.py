from django.shortcuts import render, get_object_or_404
from .models import Program, About, Actuality, Testimonial
from students.models import Students
from education.models import Options
from staff.models import Staff
from django.utils import timezone
import calendar
from django.core.paginator import Paginator

def event_404(request):
    return render(request, 'home/event/404.html')


def index(request):
    context = {
        'program': Program.objects.all()[:6],
        'about': About.objects.all()[:1],
        'actuality':Actuality.objects.all()[:4],
        'testimonial':Testimonial.objects.all()[:6],
        'year': int(timezone.now().year) - 2022,
        'option': Options.objects.all().count(),
        'students': Students.objects.all().count() if Students.objects else 0,
        'titre':'Gethsemane'            
    }
    return render(request, 'home/index.html', context)

def about(request):
    context = {
        'about': About.objects.all()[:1],
        'staffs': Staff.objects.select_related('user').all().filter(admin= 'True'),
        'year': int(timezone.now().year) - 2022,
        'staff_count': Staff.objects.all().count()         
    }
    return render(request, 'home/about.html', context)

def event(request):
    act = Actuality.objects.all().order_by("-id")

    paginator = Paginator(act, 10)
    page_number = request.GET.get("page")
    evet = paginator.get_page(page_number)
      
    context = {
        'events':evet,
        'image':Actuality.objects.all()[1:],
        'time': timezone.now(),
        'calendar': calendar.month(int(timezone.now().year), int(timezone.now().month))  
    }
    
    return render(request, 'home/events.html', context)

def category_event(request, cat):
    data={}
    for catego in  Actuality.objects.filter(category =cat ):
        data[catego.category] = []
    data[catego.category].append(str(catego.title))
         
    return render(request, 'home/event_cat.html', {'events':data})

def show_event(request, id):
    event = get_object_or_404(Actuality, pk=id)
    
    context = {
        'event': event,
    }

    return render(request, 'home/show/event.html', context)
    
        
      
    
