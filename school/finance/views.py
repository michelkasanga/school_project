from .forms import BoxForm
from collections import defaultdict
from django.shortcuts import render, get_object_or_404, redirect
from .models import Box, Fees, MonthChoice
from .forms import FeesForm
from students.models import Students
from staff.models import Staff
from django.utils import timezone
from general.models import *
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from education.models import Classes, Section, Options
from .models import Fees, MonthChoice

def role_required(role):
    def decorator(view_func):
        """
        Décorateur pour restreindre l'accès à une vue selon le rôle du staff.
        Usage : @role_required('caisse')
        """
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("⛔ vous devez etre connecté")
            if not hasattr(request.user, 'staff') or not request.user.staff.role != role:
                return HttpResponseForbidden("⛔ Accès interdit")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# @cache_page(60 * 5)  # 5 minutes
#@role_required('caisse')
def index_box(request):
    """
    Vue principale du tableau de bord caisse (finance).
    Permet de filtrer les paiements par classe, section, option, type de frais et mois.
    Affiche les totaux du jour, la pagination et un tableau regroupé par classe/section/option/mois/frais.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        HttpResponse: La page HTML du tableau de bord caisse avec filtres et pagination.
    """
    # 1. Récupération des filtres depuis la requête GET (chaque filtre est une chaîne ou vide)
    classe = request.GET.get('classe') or ''  # Nom de la classe sélectionnée
    section = request.GET.get('section') or ''  # Nom de la section sélectionnée
    option = request.GET.get('option') or ''  # Nom de l'option sélectionnée
    fees_type = request.GET.get('fees_type') or ''  # Type de frais sélectionné
    mois = request.GET.get('mois') or ''  # Mois sélectionné (numéro)

    # 2. Construction du dictionnaire de filtres pour la requête ORM
    filters = {}
    if classe:
        filters["student__classe__name"] = classe
    if section:
        filters["student__section__name"] = section
    if option:
        filters["student__option__name"] = option
    if fees_type:
        filters["fees__name"] = fees_type
    if mois:
        try:
            filters["month"] = int(mois)
        except (ValueError, TypeError):
            pass  # Ignore si le mois n'est pas convertible

    # 3. Récupération des paiements filtrés (requête optimisée, groupée par élève/frais/mois)
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paiements = (
        Box.objects
        .filter(**filters)
        .values(
            "student__id",
            "student__name",
            "student__surname",
            "student__first_name",
            "student__matricule",
            "student__classe__name",
            "student__section__name",
            "student__option__name",
            "fees__name",
            "fees__amount",
            "month",
        )
        .annotate(total=Sum("amount_pay"))
    )

    # 4. Pagination sur les paiements (avant regroupement)
    page = request.GET.get('page', 1)
    paginator = Paginator(list(paiements), 20)  # 20 lignes par page
    try:
        paiements_page = paginator.page(page)
    except PageNotAnInteger:
        paiements_page = paginator.page(1)
    except EmptyPage:
        paiements_page = paginator.page(paginator.num_pages)

    # 5. Préparation des listes pour les filtres (affichent toujours toutes les valeurs possibles)
    classes = Classes.objects.all().values_list('name', flat=True)
    sections = Section.objects.all().values_list('name', flat=True)
    options = Options.objects.all().values_list('name', flat=True)
    fees_types = Fees.objects.all().values_list('name', flat=True)
    mois_list = [m.value for m in MonthChoice]

    # 6. Regroupement des paiements de la page courante par classe/section/option/mois/frais
    #    (structure imbriquée pour affichage dans le template)
    groupe_per_classe = {}
    for paiement in paiements_page:
        classe = paiement["student__classe__name"]
        section = paiement["student__section__name"] if paiement["student__section__name"] else ""
        option = paiement["student__option__name"] if paiement["student__option__name"] else ""
        mois_val = paiement["month"]
        label_month = MonthChoice(mois_val).label
        student_id = paiement["student__id"]
        student_name = paiement["student__name"]
        student_surname = paiement["student__surname"]
        student_first_name = paiement["student__first_name"]
        matricule = paiement["student__matricule"]
        fees_name = paiement["fees__name"]
        fees_mount = paiement["fees__amount"]
        total = paiement["total"]
        rest = fees_mount - total
        # Statut de paiement (en ordre ou dette)
        statut = (
            f"En ordre avec <span style = \"  color:green;\"> {label_month} </span>" if rest == 0 else f" Une dette de <span style = \"  color:red;\">{rest} </span>"
        )
        # Détail des paiements individuels pour ce frais/mois/élève
        paiements_details = Box.objects.filter(
            student__id=student_id,
            fees__name=fees_name,
            month=mois_val
        ).values('paid_date', 'amount_pay')
        details_paiement = [
            {
                'date': p['paid_date'].strftime('%d %B %Y'),
                'montant': float(p['amount_pay'])
            }
            for p in paiements_details
        ]
        # Construction de l'objet info pour le template
        info = {
            "student_id": student_id,
            "student_name": student_name,
            "student_surname": student_surname,
            "student_first_name": student_first_name,
            "matricule": matricule,
            "fees_name": fees_name,
            "months": label_month,
            "total": total,
            "fees_mount": fees_mount,
            "statut": statut,
            "details_paiement": details_paiement,
            "dette": rest,
            "id": paiement["student__id"],
            "section": section,
            "option": option,
        }
        # Insertion dans la structure imbriquée
        if classe not in groupe_per_classe:
            groupe_per_classe[classe] = {}
        if section not in groupe_per_classe[classe]:
            groupe_per_classe[classe][section] = {}
        if option not in groupe_per_classe[classe][section]:
            groupe_per_classe[classe][section][option] = {}
        if label_month not in groupe_per_classe[classe][section][option]:
            groupe_per_classe[classe][section][option][label_month] = {}
        if fees_name not in groupe_per_classe[classe][section][option][label_month]:
            groupe_per_classe[classe][section][option][label_month][fees_name] = []
        groupe_per_classe[classe][section][option][label_month][fees_name].append(info)

    # 7. Calcul des totaux du jour (pour affichage en haut de page)
    today = timezone.localdate()
    transactions_today = Box.objects.filter(paid_date__date=today)
    total_today = transactions_today.aggregate(total=models.Sum('amount_pay'))['total'] or 0
    count_today = transactions_today.count()

    # 8. Rendu du template avec toutes les variables nécessaires
    return render(request, "finance/box.html", {
        "groupe_per_classe": groupe_per_classe,
        "classes": sorted(classes),
        "sections": sorted(sections),
        "options": sorted(options),
        "fees_types": sorted(fees_types),
        "mois_list": sorted(mois_list),
        "selected": {
            "classe": classe,
            "section": section,
            "option": option,
            "fees_type": fees_type,
            "mois": mois,
        },
        'titre':'Caisse',
        'eleves':Students.objects.all().filter(statut='scolariser'),
        "contacts": Contact.objects.all()[:1],
        "total_today": total_today,
        "count_today": count_today,
        "page_obj": paiements_page,
    })
    
def show_box(request, student_id):

    """
    Affiche le détail des paiements d'un élève, regroupés par frais et par mois.
    Permet de voir l'historique des paiements, le total payé, la dette restante, etc.

    Args:
        request (HttpRequest): La requête HTTP reçue.
        student_id (int): L'identifiant de l'élève.

    Returns:
        HttpResponse: La page HTML affichant le détail des paiements de l'élève.
    """
    paiements = Box.objects.filter(student__id=student_id)
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
    # Conversion récursive en dict pour le template
    def deep_dict(d):
        if isinstance(d, dict):
            return {k: deep_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [deep_dict(i) for i in d]
        else:
            return d
    groupe_frais_dict = deep_dict(dict(groupe_frais))
    return render(request, "finance/show_box.html", {
        "groupe_frais": groupe_frais_dict,
        'paiement':paiement
    })

def add_payment(request):
    """
    Vue pour ajouter un nouveau paiement (caisse).
    Affiche un formulaire, puis redirige vers l'impression du reçu si succès.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        HttpResponse: La page HTML du formulaire ou la redirection vers le reçu.
    """
    if request.method == 'POST':
        form = BoxForm(request.POST)
        if form.is_valid():
            payment =  form.save()
            return redirect('finance:print_receipt', payment_id=payment.id)
    else:
        form = BoxForm()
    return render(request, 'finance/add_payment_modal.html', {'form': form})

def edit_payment(request, payment_id):
    """
    Vue pour modifier un paiement existant (caisse).
    Affiche le formulaire pré-rempli, puis redirige vers la fiche élève après modification.

    Args:
        request (HttpRequest): La requête HTTP reçue.
        payment_id (int): L'identifiant du paiement à modifier.

    Returns:
        HttpResponse: La page HTML du formulaire ou la redirection vers la fiche élève.
    """
    payment = get_object_or_404(Box, pk=payment_id)
    if request.method == 'POST':
        from .forms import BoxForm
        form = BoxForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('finance:show_box', student_id=payment.student.id)
    else:
        from .forms import BoxForm
        form = BoxForm(instance=payment)
    return render(request, 'finance/edit_payment.html', {'form': form, 'payment': payment})

def print_receipt(request, payment_id):
    """
    Vue pour afficher/imprimer le reçu d'un paiement donné.
    Affiche les infos de l'élève, le montant payé, le montant attendu, le statut, etc.

    Args:
        request (HttpRequest): La requête HTTP reçue.
        payment_id (int): L'identifiant du paiement.

    Returns:
        HttpResponse: La page HTML du reçu.
    """
    payment = get_object_or_404(Box, pk=payment_id)
    student = payment.student
    total = Box.objects.filter(student=student).aggregate(total=Sum('amount_pay'))['total']
    attendu = payment.fees.amount if hasattr(payment, 'fees') else None
    statut = "Payé" if total and attendu and total >= attendu else "Partiel"
    context = {
        'nom_eleve': f"{student.name} {student.surname} {student.first_name}",
        'classe': student.classe.name if hasattr(student, 'classe') else '',
        'option': student.option.name if student.option else '',
        'matricule': student.matricule,
        'section':student.section.name if student.section else '',
        'type_frais': payment.fees.name if hasattr(payment, 'fees') else '',
        'mois': payment.get_month_display,
        'paiement': payment,
        'total': total,
        'attendu': attendu,
        'statut': statut,
    }
    return render(request, 'finance/receipt.html', context)

def index_fees(request):
    """
    Vue pour afficher la liste de tous les types de frais existants.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        HttpResponse: La page HTML listant les frais.
    """
    fees = Fees.objects.only('id', 'name', 'amount' )
    return render(request, 'finance/fees.html', {'fees': fees})

def add_fee(request):
    """
    Vue pour ajouter un nouveau type de frais.
    Affiche un formulaire, puis redirige vers la liste des frais si succès.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        HttpResponse: La page HTML du formulaire ou la redirection vers la liste des frais.
    """
    if request.method == 'POST':
        form = FeesForm(request.POST)
        if form.is_valid():
            fee = form.save()
            return redirect('finance:index_fees') # Redirige vers la fiche des frais
    else:
        form = FeesForm()
    return render(request, 'finance/add_fees.html', {'form': form})

   
def edit_fee(request, fee_id):
    """
    Vue pour modifier un type de frais existant.
    Affiche le formulaire pré-rempli, puis redirige vers la liste des frais après modification.

    Args:
        request (HttpRequest): La requête HTTP reçue.
        fee_id (int): L'identifiant du frais à modifier.

    Returns:
        HttpResponse: La page HTML du formulaire ou la redirection vers la liste des frais.
    """
    fee = get_object_or_404(Fees, pk=fee_id)
    if request.method == 'POST':
        form = FeesForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            return redirect('finance:index_fees' ) # Redirige vers la fiche élève, à adapter si besoin
    else:
        form = FeesForm(instance=fee)
    return render(request, 'finance/edit_fee.html', {'form': form, 'fee': fee})


def delete_fees(request, fee_id):
    """
    Vue pour supprimer un type de frais existant.
    Supprime le frais après confirmation POST, puis redirige vers la liste des frais.

    Args:
        request (HttpRequest): La requête HTTP reçue.
        fee_id (int): L'identifiant du frais à supprimer.

    Returns:
        HttpResponse: Redirection vers la liste des frais après suppression.
    """
    fee = get_object_or_404(Fees, pk=fee_id)
    if request.method == 'POST':
        fee.delete()
        return redirect('finance:index_fees')
   



