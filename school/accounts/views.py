"""
Vues pour la gestion des comptes utilisateurs (connexion, profils, déconnexion, etc.).
Chaque fonction est documentée selon les standards Pylint.
"""

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
from collections import defaultdict



def login_view(request):
    """
    Vue de connexion utilisateur. Authentifie l'utilisateur et redirige selon son profil (staff ou élève).
    Args:
        request (HttpRequest): La requête HTTP reçue.
    Returns:
        HttpResponse: Page de connexion ou redirection vers le profil.
    """
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
    return render(request, "accounts/login.html", {'form':form})

def profile(request, user_id):
    """
    Vue pour afficher le profil d'un utilisateur staff.
    Args:
        request (HttpRequest): La requête HTTP reçue.
        user_id (int): L'identifiant de l'utilisateur.
    Returns:
        HttpResponse: Page de profil staff.
    """
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
    return render(request, "profiles/profile.html", context)

@login_required
def edit_profile(request, user_id):
    """
    Vue pour modifier le profil d'un utilisateur staff.
    Args:
        request (HttpRequest): La requête HTTP reçue.
        user_id (int): L'identifiant de l'utilisateur.
    Returns:
        HttpResponse: Page d'édition du profil ou redirection après modification.
    """
    profile = Profiles.objects.get(user_id=user_id)
    if request.method == 'POST':
        form = ProfilesForm(request.POST, request.FILES, instance= profile)
        
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', user_id = user_id)
    else:
        form = ProfilesForm(instance=profile)
    return render(request, 'profiles/edit.html', {'form':form})

def logout_view(request):
    """
    Déconnecte l'utilisateur et redirige vers la page d'accueil.
    Args:
        request (HttpRequest): La requête HTTP reçue.
    Returns:
        HttpResponse: Redirection vers la page d'accueil.
    """
    logout(request)
    return redirect('general:index')

# @login_required
def profile_students(request, user_id):
    """
    Vue pour afficher le profil d'un élève et son historique de paiements.
    Args:
        request (HttpRequest): La requête HTTP reçue.
        user_id (int): L'identifiant de l'utilisateur élève.
    Returns:
        HttpResponse: Page de profil élève avec paiements.
    """
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
    
    
    paiements = Box.objects.filter(student__id=students.id)# Récupérer tous les paiements de l'élève
    # Regrouper par frais et mois
    groupe_frais = defaultdict(lambda: defaultdict(list))
    # Regroupement unique par frais/mois
    unique_frais_mois = {}
    for paiement in paiements:
        mois_val = paiement.month
        fees_name = paiement.fees.name
        fee_id = paiement.fees.id
        key = f"{fees_name}_{mois_val}"
        if key not in unique_frais_mois:
            unique_frais_mois[key] = {
                "student_id": paiement.student.id,
                "student_name": paiement.student.name,
                "student_surname": paiement.student.surname,
                "student_first_name": paiement.student.first_name,
                "fees_name": fees_name,
                "months": mois_val,
                "fees_mount": float(paiement.fees.amount),
                "details_paiement": [],
                "fee_id": fee_id,
            }
        unique_frais_mois[key]["details_paiement"].append({
            'date': paiement.paid_date.strftime('%d %B %Y'),
            'montant': float(paiement.amount_pay),
            'payment_id': paiement.id
        })
    # Calcul total et dette pour chaque frais/mois
    groupe_frais = {}
    for info in unique_frais_mois.values():
        total = sum([p['montant'] for p in info['details_paiement']])
        rest = info['fees_mount'] - total
        info['total'] = total
        info['dette'] = rest
        info['statut'] = f"En ordre avec le mois de {info['months']}" if rest == 0 else f"Une dette de {rest}"
        frais_name = info['fees_name']
        mois_val = info['months']
        if frais_name not in groupe_frais:
            groupe_frais[frais_name] = {}
        groupe_frais[frais_name][mois_val] = [info]
    # Conversion en dict pour le template
    def deep_dict(d):
        if isinstance(d, dict):
            return {k: deep_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [deep_dict(i) for i in d]
        else:
            return d
    groupe_frais_dict = deep_dict(dict(groupe_frais))
    
    context = {
         "groupe_frais": groupe_frais_dict,
        'paiement':paiement,
        "contacts": Contact.objects.all()[:1],
        'profile':profile,
        'students':students, 
        'age': today.year - students.date_birthday.year if students.date_birthday  else '-' 
    }
 
    return render(request, "profiles/profile_students.html", context)

