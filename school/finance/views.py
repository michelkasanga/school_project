from django.shortcuts import render, get_object_or_404
from .models import Box, Fees
from students.models import Students
from staff.models import Staff
from django.db.models import Sum


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
            f"En ordre avec le mois de {mois_val}" if rest == 0
            else f"Une dette de {rest}"
        )

        info = {
            "student_id": student_id,
            "student_name": student_name,
            "student_surname": student_surname,
            "student_first_name": student_first_name,
            "fees_name": fees_name,
            "months": mois_val,
            "total": total,
            "fees_mount": fees_mount,
            "statut": statut,
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
            groupe_per_classe[classe][section][option][mois_val] = {}
        if fees_name not in groupe_per_classe[classe][section][option][mois_val]:
            groupe_per_classe[classe][section][option][mois_val][fees_name] = []

        groupe_per_classe[classe][section][option][mois_val][fees_name].append(info)

    return render(request, "home/box/box.html", {
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
        'eleves':Students.objects.all().filter(statut='scolariser')
    })
    


def show_box(request, eleve_id):
    eleve = get_object_or_404(Students, id=eleve_id)
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
        "nom_eleve": eleve.name,
        "classe": eleve.classe.name, # ⚠️ adapte si ton Student n’a pas ce champ
        "type_frais": type_frais,
        "mois": mois,
        "paiements": details,
        "total": total,
        "attendu": attendu,
        "statut": statut,
    }
    
    return render(request, "home/show_box.html", context)