from django.shortcuts import render, get_object_or_404
from .models import Box, Fees
from students.models import Students
from staff.models import Staff


def index_box(request):
    #recuperation de tout les paiement
    paiements = Box.objects.select_related('student', 'fees').all()
    
    groupe_per_classe = {}
    
    for paiement in paiements:
        classe = paiement.student.classe.name
        student_name = paiement.student.name
        fees_name = paiement.fees.name
        months = paiement.month
        
        #montant attendu
        fees_mount = paiement.fees.amount
        
        #total payé par eleve
        total = Box.objects.filter(
            student = paiement.student,
            fees = paiement.fees,
            month = paiement.month,
        ).aaggregate(total = sum("amount_pay"))["total"] or 0
        
        rest = fees_mount - total
        statut = (
            f"En ordre avec le mois de {months}"
            if rest == 0
            else f"une dette de {rest}"
        )
        
        info = {
            'student_name': student_name,
            'fees_name': fees_name,
            'months' : months,
            'total':total,
            'fees_mount':fees_mount,
            'statut':statut,
            'lien':f"/show/{paiement.student.id}/"
        }
        
        if classe not in groupe_per_classe:
            groupe_per_classe[classe] = []
        if info not in groupe_per_classe[classe]:
            groupe_per_classe[classe].append(info)
            
    return render(request, "home/box.html", {"groupe_per_classe": groupe_per_classe})
    


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
        "nom_eleve": eleve.nom,
        "classe": eleve.classe.nom,   # ⚠️ adapte si ton Student n’a pas ce champ
        "type_frais": type_frais,
        "mois": mois,
        "paiements": details,
        "total": total,
        "attendu": attendu,
        "statut": statut,
    }
    
    return render(request, "home/show_box.html", context)