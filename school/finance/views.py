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

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("⛔ vous devez etre connecté")
            if not hasattr(request.user, 'staff') or not request.user.staff.role != role:
                return HttpResponseForbidden("⛔ Accès interdit")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@cache_page(60 * 5)  # 5 minutes
#@role_required('caisse')
def index_box(request):
    # Récupérer les filtres depuis la requête GET
    classe = request.GET.get('classe')
    section = request.GET.get('section')
    option = request.GET.get('option')
    fees_type = request.GET.get('fees_type')
    mois = request.GET.get('mois')

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
        filters["month"] = mois

    paiements = (
        Box.objects
        .filter(**filters)
        .values(
            "student__id",
            "student__name",
            "student__surname",
            "student__first_name",
            "student__classe__name",
            "student__section__name",
            "student__option__name",
            "fees__name",
            "fees__amount",
            "month",
        )
        .annotate(total=Sum("amount_pay"))
    )

    groupe_per_classe = {}
    # Pour les filtres dynamiques
    classes = set()
    sections = set()
    options = set()
    fees_types = set()
    mois_list = set()

    for paiement in paiements:
        classe = paiement["student__classe__name"]
        section = paiement["student__section__name"] if paiement["student__section__name"] else ""
        option = paiement["student__option__name"] if paiement["student__option__name"] else ""
        mois_val = paiement["month"]
        label_month = MonthChoice(mois_val).label

        # Ajout pour les filtres
        if classe: classes.add(classe)
        if section: sections.add(section)
        if option: options.add(option)
        if paiement["fees__name"]: fees_types.add(paiement["fees__name"])
        if mois_val: mois_list.add(mois_val)
        student_id = paiement["student__id"]
        student_name = paiement["student__name"]
        student_surname = paiement["student__surname"]
        student_first_name = paiement["student__first_name"]
        fees_name = paiement["fees__name"]
        fees_mount = paiement["fees__amount"]
        total = paiement["total"]

        rest = fees_mount - total
        statut = (
            f"En ordre avec {label_month}" if rest == 0 else f"Une dette de {rest}"
        )

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

        info = {
            "student_id": student_id,
            "student_name": student_name,
            "student_surname": student_surname,
            "student_first_name": student_first_name,
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

        if classe not in groupe_per_classe:
            groupe_per_classe[classe] = {}
        if section not in groupe_per_classe[classe]:
            groupe_per_classe[classe][section] = {}
        if option not in groupe_per_classe[classe][section]:
            groupe_per_classe[classe][section][option] = {}
        if mois_val not in groupe_per_classe[classe][section][option]:
            groupe_per_classe[classe][section][option][label_month] = {}
        if fees_name not in groupe_per_classe[classe][section][option][label_month]:
            groupe_per_classe[classe][section][option][label_month][fees_name] = []

        groupe_per_classe[classe][section][option][label_month][fees_name].append(info)

    
    today = timezone.localdate()
    transactions_today = Box.objects.filter(paid_date__date=today)
    total_today = transactions_today.aggregate(total=models.Sum('amount_pay'))['total'] or 0
    count_today = transactions_today.count()
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
    })
    
def show_box(request, student_id):

    paiements = Box.objects.filter(student__id=student_id)# Récupérer tous les paiements de l'élève
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
    return render(request, "finance/show_box.html", {
        "groupe_frais": groupe_frais_dict,
    })

def add_payment(request):
    if request.method == 'POST':
        form = BoxForm(request.POST)
      
        if form.is_valid():
            payment =  form.save()
            return redirect('finance:print_receipt', payment_id=payment.id)
    else:
        form = BoxForm()
    return render(request, 'finance/add_payment_modal.html', {'form': form})

def edit_payment(request, payment_id):
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
    fees = Fees.objects.only('id', 'name', 'amount' )
    return render(request, 'finance/fees.html', {'fees': fees})

def add_fee(request):
    if request.method == 'POST':
        form = FeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance:index_fees') # Redirige vers la fiche des frais
    else:
        form = FeesForm()
    return render(request, 'finance/add_fees.html', {'form': form})

   
def edit_fee(request, fee_id):
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
    fee = get_object_or_404(Fees, pk=fee_id)
    if request.method == 'POST':
        fee.delete()
        return redirect('finance:index_fees')
   



