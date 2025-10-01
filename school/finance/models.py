"""
Modèles pour la gestion financière (frais, paiements, caisse, etc.).
Chaque classe et méthode est documentée selon les standards Pylint.
"""

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
from education.models import *
from students.models import Students
from staff.models import Staff



class MonthChoice(models.IntegerChoices):
    """
    Enumération des mois utilisés pour les paiements.
    """
    SEPTEMBRE = 1, 'Septembre'
    OCTOBRE = 2, 'Octobre'   
    NOVEMBRE = 3, 'Novembre'
    DECEMBRE = 4, 'Décembre'
    JANVIER = 5, 'Janvier'
    FEVRIER = 6, 'Février'
    MARS = 7, 'Mars'
    AVRIL = 8, 'Avril'
    MAI = 9, 'Mai'
    JUIN = 10, 'Juin'


class Fees(models.Model):
    """
    Modèle représentant un type de frais scolaire (montant, classe, section, options).
    """
    name = models.CharField("Frais",max_length=100, unique=False, null=False, blank=False)
    amount = models.DecimalField("Montant",max_digits=10, decimal_places=2, null=False, blank=False)
    classe = models.ManyToManyField(Classes)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    options = models.ManyToManyField(Options, blank=True)
    created_at = models.DateTimeField("Creation",auto_now_add=True)
    updated_at = models.DateTimeField("Modification",auto_now=True)
    
    class Meta:
        db_table='fees'
        verbose_name = 'frais'
        verbose_name_plural = 'frais'
        ordering = ['updated_at']  
    
    def __str__(self):
        """
        Retourne le nom et le montant du frais.
        Returns:
            str: Description du frais.
        """
        return f"{self.name} {self.amount}"
    
    def formatted_created_at(self):
        """
        Retourne la date de création formatée.
        Returns:
            str: Date formatée.
        """
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def formatted_updated_at(self):
        """
        Retourne la date de mise à jour formatée.
        Returns:
            str: Date formatée.
        """
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
    
    #__________________________________________
class Box(models.Model):
    """
    Modèle représentant un paiement effectué par un élève pour un frais donné et un mois donné.
    """
    TYPE_PAIEMENT_CHOICES = [
        ('espece', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement'),
        ('carte', 'Carte bancaire'),
    ]
    
    student = models.ForeignKey(Students, on_delete= models.CASCADE, null=False, blank=False )
    fees = models.ForeignKey(Fees, on_delete= models.CASCADE, null=False, blank=False )
    amount_pay = models.DecimalField("Montant", max_digits=10, decimal_places=2)
    month = models.IntegerField('Mois', choices=MonthChoice.choices, default=MonthChoice.SEPTEMBRE)
    type_paiement = models.CharField("Type de paiement",max_length=20, choices=TYPE_PAIEMENT_CHOICES, default='espece')
    collector = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, editable=False)
    paid_date = models.DateTimeField("Date de paiment",auto_now_add=True)
    updated_at = models.DateTimeField("Modification",auto_now=True)
    
    class Meta:
        db_table='box'
        verbose_name = "Caisse"
        verbose_name_plural="caisse"
        
    def get_month_display(self):
        """
        Retourne le nom du mois correspondant à la valeur stockée.
        Returns:
            str: Nom du mois ou '-'.

        """
        return MonthChoice(self.month).label if self.month in MonthChoice.values else '-'

    def __str__(self):
        """
        Retourne une description textuelle du paiement.
        Returns:
            str: Description du paiement.
        """
        return f"{self.student} - {self.fees.name} - {self.get_month_display()}"
    
        
    def add_payment(self, *amount):
        """
        Ajoute un paiement pour l'élève, le frais et le mois courant (stocké comme entier).
        Si le total payé atteint le montant du frais, l'excédent est reporté sur le mois suivant.
        Le champ 'mois' de chaque paiement créé correspond bien à l'indice du mois concerné.
        L'élève ne peut pas payer plus que le montant total fixé dans Fees pour chaque mois.
        """
        from django.db import transaction
        from decimal import Decimal
        months = list(MonthChoice.values)
        try:
            current_month_index = months.index(self.month)
        except ValueError:
            current_month_index = self.month - 1
        total_fees = self.fees.amount
        student = self.student
        fees = self.fees
        remaining_amount = Decimal(amount)
        while remaining_amount > 0 and current_month_index < len(months):
            month_idx = months[current_month_index]
            total_paid = Box.objects.filter(student=student, fees=fees, month=month_idx).aggregate(models.Sum('amount_pay'))['amount_pay__sum'] or Decimal('0.0')
            to_pay = total_fees - total_paid
            if to_pay <= 0:
                current_month_index += 1
                continue
            pay_now = min(remaining_amount, to_pay)
            with transaction.atomic():
                Box.objects.create(
                    student=student,
                    fees=fees,
                    amount_pay=pay_now,
                    month=month_idx,
                    type_paiement=self.type_paiement,
                    collector=self.collector
                )
            remaining_amount -= pay_now
            current_month_index += 1
        return True
   
        
class Total(models.Model):
    """
    Modèle représentant le total des paiements pour un frais et un mois donnés.
    """
    @classmethod
    def update_totals_for_fees_and_month(cls, fees, month):
        """
        Met à jour les totaux pour un frais et un mois donnés.
        Args:
            cls: La classe en cours (Total).
            fees (Fees): L'objet frais associé.
            month (int): Le mois pour lequel mettre à jour les totaux.
        """
        from .models import Box  # Import différé pour éviter les problèmes de dépendance
        from django.db.models import Sum
        from decimal import Decimal
        
        total_pay = Box.objects.filter(fees=fees, month=month).aggregate(Sum('amount_pay'))['amount_pay__sum'] or 0
        nbrStudents = Box.objects.filter(fees=fees, month=month).values('student').distinct().count()
        # Le montant total à payer ne doit pas dépasser le montant du fees * nombre d'élèves
        total_amount = nbrStudents * float(fees.amount)
        # On limite le total payé au maximum autorisé
        total_pay_capped = min(float(total_pay), total_amount)
        reste = total_amount - total_pay_capped
        if reste < 0:
            reste = 0
        statut = (reste == 0)
        total_obj, created = cls.objects.get_or_create(fees=fees, month=month, defaults={
            'nbrStudents': nbrStudents,
            'total_pay': total_pay_capped,
            'total_amount': total_amount,
            'reste': reste,
            'statut': statut
        })
        if not created:
            total_obj.nbrStudents = nbrStudents
            total_obj.total_pay = total_pay_capped
            total_obj.total_amount = total_amount
            total_obj.reste = reste
            total_obj.statut = statut
            total_obj.save()
    fees = models.ForeignKey(Fees, on_delete= models.CASCADE, null=False, blank=False )
    month = models.IntegerField('Mois', choices=MonthChoice.choices, default=MonthChoice.SEPTEMBRE)
    nbrStudents = models.IntegerField("Nombre d'élèves", default=0)
    total_pay = models.DecimalField("Total payer", max_digits=10, decimal_places=2, default=0.0)
    total_amount = models.DecimalField("Total frais", max_digits=10, decimal_places=2, default=0.0)
    reste = models.DecimalField("Reste à payer", max_digits=10, decimal_places=2, default=0.0)
    statut = models.BooleanField("Statut", default=False)
    updated_at = models.DateTimeField("Modification",auto_now=True)
    
    class Meta:
        db_table='total'
        verbose_name = "Total"
        
    def get_month_display(self):
        """
        Retourne le nom du mois correspondant à la valeur stockée.
        Returns:
            str: Nom du mois ou '-'.
        """
        return MonthChoice(self.month).label if self.month in MonthChoice.values else '-'

    def __str__(self):
        """
        Retourne une description textuelle du total.
        Returns:
            str: Description du total.
        """
        return f"{self.fees.name} - {self.get_month_display()}"
# Signaux pour mettre à jour Total à chaque ajout, modification ou suppression de Box

# Signaux pour mettre à jour Total à chaque ajout, modification ou suppression de Box
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Box)
@receiver(post_delete, sender=Box)
def update_total_on_box_change(sender, instance, **kwargs):
    """
    Met à jour le total associé à un paiement lorsque celui-ci est ajouté, modifié ou supprimé.
    Args:
        sender (Model): Le modèle qui envoie le signal.
        instance (Box): L'instance de Box qui a été modifiée.
        **kwargs: Arguments supplémentaires.
    """
    Total.update_totals_for_fees_and_month(instance.fees, instance.month)

    @classmethod
    def update_totals_for_fees_and_month(cls, fees, month):
        """
        Met à jour les totaux pour un frais et un mois donnés.
        Args:
            cls: La classe en cours (Total).
            fees (Fees): L'objet frais associé.
            month (int): Le mois pour lequel mettre à jour les totaux.
        """
        from .models import Box  # Import différé pour éviter les problèmes de dépendance
        from django.db.models import Sum
        from decimal import Decimal
        
        total_pay = Box.objects.filter(fees=fees, month=month).aggregate(Sum('amount_pay'))['amount_pay__sum'] or 0
        nbrStudents = Box.objects.filter(fees=fees, month=month).values('student').distinct().count()
        # Le montant total à payer ne doit pas dépasser le montant du fees * nombre d'élèves
        total_amount = nbrStudents * float(fees.amount)
        # On limite le total payé au maximum autorisé
        total_pay_capped = min(float(total_pay), total_amount)
        reste = total_amount - total_pay_capped
        if reste < 0:
            reste = 0
        statut = (reste == 0)
        total_obj, created = cls.objects.get_or_create(fees=fees, month=month, defaults={
            'nbrStudents': nbrStudents,
            'total_pay': total_pay_capped,
            'total_amount': total_amount,
            'reste': reste,
            'statut': statut
        })
        if not created:
            total_obj.nbrStudents = nbrStudents
            total_obj.total_pay = total_pay_capped
            total_obj.total_amount = total_amount
            total_obj.reste = reste
            total_obj.statut = statut
            total_obj.save()




