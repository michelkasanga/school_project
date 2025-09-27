from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profiles
from django.contrib import messages
from staff.models import Staff
from students.models import Students
from education.models import Courses
from .forms import CustomLoginForm, ProfilesForm
from django.utils import timezone
from datetime import date 
from finance.models import Box, Fees
from staff.models import Staff
from general.models import * 



def login_view(request):
    if request.method == 'POST':
       form = CustomLoginForm(request.POST)
       if form.is_valid():
           username = form.cleaned_data.get("username")
           password = form.cleaned_data.get("password")
           user = authenticate(username=username, password=password)
           if user is not None :
               login(request, user)
               try:
                   Staff.objects.get(user=user)
                   return redirect('accounts:profile', user_id = user.id) 
               except Staff.DoesNotExist:
                   pass
               
               try:
                   Students.objects.get(user=user)
                   return redirect('accounts:profile_students', user_id = user.id) 
               except Students.DoesNotExist:
                   pass
               
               return redirect('accounts:profile', user_id = user.id) 
                           
           else:
                messages.success(request, f"mauvaise identification")    
    else:
        
        form = CustomLoginForm()
    return render(request, "home/accounts/login.html", {'form':form})

def profile(request, user_id):
    
    user = get_object_or_404(User, id=user_id)
    try:
        staff = Staff.objects.get(user=user)
    except Staff.DoesNotExist:
        staff = None
        
    try:
        profile = Profiles.objects.get(user=user)
    except Profiles.DoesNotExist:
        profile = None    
        
    try:
        caisse = Staff.objects.filter(role__name = 'caisse').exists()
    except Staff.DoesNotExist:
        caisse = None 
        
    if staff is not None:
       cours = Courses.objects.only('id').filter(professor_id=staff.id)
    else:
        cours=[]
   
     
    context={
        'profile':profile,
        'staff': staff ,
        'caisse':caisse, 
        'cours':cours
    }
    return render(request, "home/profiles/profile.html", context)

@login_required
def edit_profile(request, user_id):
    profile = Profiles.objects.get(user_id=user_id)
    if request.method == 'POST':
        form = ProfilesForm(request.POST, request.FILES, instance= profile)
        
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', user_id = user_id)
    else:
        form = ProfilesForm(instance=profile)
    return render(request, 'home/profiles/edit.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('general:index')

@login_required
def profile_students(request, user_id):
    
    user = get_object_or_404(User, id=user_id)
    try:
        students = Students.objects.get(user=user)
    except Students.DoesNotExist:
        students = None
        
    try:
        profile = Profiles.objects.get(user=user)
    except Profiles.DoesNotExist:
        profile = None    
 
    today = date.today()
    
    eleve = students
    paiements = Box.objects.filter(student= eleve).select_related("fees")
    
    details = []
    total = 0
    attendu = 0
    mois = None
    type_frais = None
    
    for p in paiements:
        details.append({
            "date":p.paid_date.strftime("%d %B %Y"),
            "mois":p.month,
            "montant":p.amount_pay,
        })
        
        total += p.amount_pay
        attendu = p.fees.amount
        mois = p.month
        type_frais = p.fees.name
        
    reste = attendu - total
    statut = f"En ordre avec le mois de {mois}" if reste == 0 else f"Une dette de {reste}"
    context = {
         # ⚠️ adapte si ton Student n’a pas ce champ
        "type_frais": type_frais,
        "mois": mois,
        "paiements": details,
        "total": total,
        "attendu": attendu,
        "statut": statut,
        "contacts": Contact.objects.all()[:1],
        'profile':profile,
        'students':students, 
        'age': today.year - students.date_birthday.year if students.date_birthday  else '-' 
    }
 
    return render(request, "home/profiles/profile_students.html", context)
    
