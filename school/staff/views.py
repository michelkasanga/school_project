
"""
Vues pour la gestion du staff et des doyens dans l'application scolaire.
Chaque fonction est documentée selon les standards Pylint.
"""

from django.shortcuts import render, get_object_or_404
from .models import Staff, Dean
from general.models import *
from django.core.paginator import Paginator



def dean(request):

    """
    Vue pour afficher la liste des doyens, groupés par option.
    Si un paramètre GET 'option' est fourni, filtre les doyens par cette option.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        HttpResponse: La page HTML affichant les doyens groupés par option.
    """
    # Récupère l'ID de l'option depuis les paramètres GET (si présent)
    option_id = request.GET.get('option')
    queryset = Dean.objects.select_related('staff', 'option')
    if option_id:
        queryset = queryset.filter(option_id=option_id)

    # Grouper les doyens par option dans un dictionnaire ordonné
    from collections import OrderedDict
    options_dict = OrderedDict()
    for dean_obj in queryset:
        option = dean_obj.option
        if option not in options_dict:
            options_dict[option] = []
        options_dict[option].append(dean_obj.staff)

    context = {
        'options': options_dict,
    }
    return render(request, 'staff/dean.html', context)


def staff(request):

    """
    Vue pour afficher la liste paginée de tout le staff de l'école.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        HttpResponse: La page HTML affichant le staff paginé.
    """
    # Récupère uniquement les champs nécessaires pour l'affichage
    staff_qs = Staff.objects.only('id', 'name', 'surname', 'firstname', 'title', 'role')
    paginator = Paginator(staff_qs, 10)

    # Numéro de page depuis les paramètres GET
    page_number = request.GET.get("page")
    staffs = paginator.get_page(page_number)

    context = {
        'staffs': staffs,
        'titre': "Staff",
    }

    return render(request, 'staff/staff.html', context)
