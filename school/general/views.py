from django.shortcuts import render, get_object_or_404
from .models import Program, About, Actuality, Testimonial, Hero, Contact, CategorieEvenement
from students.models import Students
from education.models import Options
from staff.models import Staff
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count, Sum

def event_404(request):
    return render(request, 'home/event/404.html')


def index(request):
    context = {
        'program': Program.objects.only('id', 'title', 'credit', 'duration', 'level', 'description', 'image')[:6],
        'program_count': Program.objects.count(),
        'about': About.objects.only('id', 'description').first(),
        'actuality':Actuality.objects.only('id', 'title', 'image')[:4],
        'testimonial':Testimonial.objects.only('id', 'content', 'role')[:6],
        'year': int(timezone.now().year) - 2022,
        'option': Options.objects.count(),
        'students': Students.objects.count() if Students.objects else 0,
        'hr': Hero.objects.only('id','title' ,'message', 'video').first(),
        'principal':Staff.objects.prefetch_related('role').filter(role__name = 'principal').only('id', 'role').first(),
        'titre':'Gethsemane'            
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'about': About.objects.only('id', 'description', 'image').first(),
        'staffs': Staff.objects.select_related('user').filter(admin= 'True').only('id', 'user', 'admin'),
        'year': int(timezone.now().year) - 2022,
        'staff_count': Staff.objects.count() ,      
    }
    return render(request, 'general/about.html', context)

def event(request):
    act = Actuality.objects.only('id', 'title', 'place', 'hours', 'facilitator', 'date', 'end', 'image').order_by("-id")
    category = Actuality.objects.values(
        'category'
    ).annotate(nombre = Count('id'))
    
    label_category = []
    for cate in category:
        key = cate['category']
        label = CategorieEvenement(key).label
        
        label_category.append(
            {
                'key':key,
                'label':label, 
                'nombre':cate['nombre']
            }
        )
    
    
    

    paginator = Paginator(act, 10)
    page_number = request.GET.get("page")
    evet = paginator.get_page(page_number)
      
    context = {
        'events':evet,
        'image':Actuality.objects.only('id', 'image')[1:],
        'time': timezone.now(),
        'categories':label_category,
         'all': Actuality.objects.count(),
    }
    return render(request, 'general/events.html', context)

def filter_categories(request, category):
    act = Actuality.objects.filter(category = category)
    category = Actuality.objects.values(
        'category'
    ).annotate(nombre = Count('id'))
    
    label_category = []
    for cate in category:
        key = cate['category']
        label = CategorieEvenement(key).label
        
        label_category.append(
            {
                'key':key,
                'label':label, 
                'nombre':cate['nombre'], 

            }
        )
    
    
    

    paginator = Paginator(act, 10)
    page_number = request.GET.get("page")
    evet = paginator.get_page(page_number)
      
    context = {
        'events':evet,
        'image':Actuality.objects.only('id', 'image')[1:],
        'time': timezone.now(),
        'categories':label_category, 
        'all': Actuality.objects.count()
    }
    return render(request, 'general/events_category.html', context)
    


def show_event(request, id):
    event = get_object_or_404(Actuality, pk=id)
    relate_event = Actuality.objects.filter(category = event.category).exclude(id=event.id).only('id', 'title', 'place', 'hours', 'date', 'end')
    context = {
        'event': event,
        'titre':event.title,
        'relate_event':relate_event
    }
    return render(request, 'show/event.html', context)

def program(request):
    icons = ['briefcase','graph-up', 'diagram-3', 'globe', 'cloud', 'cpu', 'tree', 'people']
    context={
        'program' : Program.objects.only('id', 'title', 'credit', 'duration', 'level', 'description', 'image'), 
        'icons' : icons,
    }
    return render(request, 'general/program.html', context)

def program_view(request, id):
    program= get_object_or_404(Program, pk=id)
    context = {
        "program": program,
        'titre':program.title
    }
    
    return render(request, 'show/program.html', context)

def contacts(request):
    context={
        "contactw": Contact.objects.only('id', 'email', 'address').first()
    }
    
        
    return render(request, 'general/contact.html', context)
    
