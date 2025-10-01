from django.db import models
from  staff.models import Staff
from tinymce.models import HTMLField
from phonenumber_field.modelfields import PhoneNumberField

"""
program = title, credit, duration, description, image
testimonial = fullname, role, content, image
actuality = title, facilitator, description, image, date, place, category, hours
about = description, image
service = name, description, image
"""

class CategorieEvenement(models.TextChoices):
    # 🎉 Divertissement & Culture
    DIV_FESTIVAL = "DIV_FESTIVAL", "Festivals"
    DIV_THEATRE = "DIV_THEATRE", "Théâtre & spectacles"
    DIV_CINEMA = "DIV_CINEMA", "Cinéma & projections"
    DIV_EXPO = "DIV_EXPO", "Expositions & musées"
    DIV_MODE = "DIV_MODE", "Mode & défilés"

    # 📚 Éducation & Formation
    EDU_CONF = "EDU_CONF", "Conférences"
    EDU_ATELIER = "EDU_ATELIER", "Ateliers / Workshops"
    EDU_COURS = "EDU_COURS", "Cours & Formations"
    EDU_LIVRE = "EDU_LIVRE", "Lancements de livres"

    # 🏢 Professionnel & Business
    BUS_FORUM = "BUS_FORUM", "Forums"
    BUS_SALON = "BUS_SALON", "Salons professionnels"
    BUS_NET = "BUS_NET", "Networking"

    # ⚽ Sport & Loisirs
    SPO_MATCH = "SPO_MATCH", "Matchs & compétitions"
    SPO_TOURNOI = "SPO_TOURNOI", "Tournois"
    SPO_RANDO = "SPO_RANDO", "Randonnées"

    # 💒 Vie sociale & personnelle
    SOC_MARIAGE = "SOC_MARIAGE", "Mariages"
    SOC_ANNIV = "SOC_ANNIV", "Anniversaires"
    SOC_SOIREE = "SOC_SOIREE", "Rencontres & soirées"

    # 🌍 Communauté & Société
    COM_MANIF = "COM_MANIF", "Manifestations / Marches"
    COM_FONDS = "COM_FONDS", "Collectes de fonds"
    COM_CARIT = "COM_CARIT", "Actions caritatives"
    COM_ASSO = "COM_ASSO", "Événements associatifs"

   

    # 🖥️ Technologie & Innovation
    #TEC_HACK = "TEC_HACK", "Hackathons"
    #TEC_LANCEMENT = "TEC_LANCEMENT", "Lancements technologiques"
    #TEC_CONF = "TEC_CONF", "Conférences IT"
    #TEC_GAMING = "TEC_GAMING", "E-sport & Gaming"


class Hero(models.Model):
    """
    Modèle représentant la section héro de la page d'accueil.
    """
    title = models.CharField("titre", max_length= 100)
    message = models.TextField("message", max_length= 500, blank=False)
    video = models.FileField(upload_to="hero/", default="hero/default.mp4")
    open_date = models.DateTimeField('date d\'ouverture')
    close_date = models.DateTimeField('date de cloture')
    register_date = models.DateTimeField('date d\'inscription')
    
    class Meta:
        db_table = 'Hero'
        verbose_name = 'Bienvenu'
        
        
class Contact(models.Model):
    """
    Modèle représentant les informations de contact de l'établissement.
    """
    email = models.EmailField()
    tel = PhoneNumberField("Téléphone", region='CD' ,null= True, blank= True, unique= True)
    address = models.TextField('Adresse', blank=False)
    hours_operation = HTMLField('Heure de travail', blank=True)
        
    
    

class Program(models.Model):
    """
    Modèle représentant un programme de formation.
    """
    title = models.CharField("Titre",max_length=100)
    credit = models.DecimalField("Credit",max_digits=10,null=True, default= 0.0, decimal_places= 2)
    duration = models.CharField("Durée",max_length=60)
    level = models.CharField("Niveau",max_length=100 , null=True)
    description = HTMLField("Description", null=True)
    condition = models.TextField(null=True)
    image = models.ImageField(upload_to='program_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    
    
    class Meta:
        db_table = 'program'
        verbose_name = 'Programme'
        verbose_name_plural = 'Programmes'
        
    def __str__(self):
        """
        Retourne le titre du programme.
        Returns:
            str: Titre du programme.
        """
        return self.title


class Testimonial(models.Model):
    """
    Modèle représentant un témoignage d'un élève ou parent.
    """
    ROLE_CHOISE = (
        ('parent', 'Parent'), 
        ('almni', 'Ancien élève'),
        ('student', 'Elève'),
        ('staff', 'cadre')
    )
    
    fullname = models.CharField("Temoin",max_length=100)
    role = models.CharField("Role",max_length=60, choices=ROLE_CHOISE)
    content = HTMLField("Temoignage", null=True)
    image = models.ImageField(upload_to='testimonial_images/', null=True)
    
    class Meta:
        db_table = 'testimonial'
        verbose_name = 'Témoignage'
        verbose_name_plural = 'Témoignages'
        
    def __str__(self):
        """
        Retourne le nom de l'auteur du témoignage.
        Returns:
            str: Nom de l'auteur.
        """
        return self.fullname

    def formatted_created_at(self):
        """
        Retourne la date de création formatée.
        Returns:
            str: Date formatée.
        """
        if self.created_at:
            return self.created_at.strftime("%d/%m/%Y %H:%M")
        return ""

    def formatted_updated_at(self):
        """
        Retourne la date de mise à jour formatée.
        Returns:
            str: Date formatée.
        """
        if self.updated_at:
            return self.updated_at.strftime("%d/%m/%Y %H:%M")
        return ""

class Actuality(models.Model):
    """
    Modèle représentant une actualité publiée par l'établissement.
    """
    title = models.CharField("Titre",max_length=100)
    facilitator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    hours = models.TimeField(null=True)
    place = models.CharField("Lieu",max_length= 100, null=True)
    category = models.CharField("Categorie",max_length=255 ,choices= CategorieEvenement.choices, default= "DIV_FESTIVAL" , null=True )
    date = models.DateTimeField('date et heure d\'ouverture', null=True)
    end = models.TimeField("heure de cloture", null=True)
    image = models.ImageField(upload_to='actuality_images/', null=True)
    description = HTMLField("Description", null=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
     
    class Meta:
        db_table = 'actuality'
        verbose_name = 'Evenement'
        verbose_name_plural = 'Evenements'
        
        
    def __str__(self):
        """
        Retourne le titre de l'actualité.
        Returns:
            str: Titre de l'actualité.
        """
        return self.title

    def formatted_created_at(self):
        """
        Retourne la date de création formatée.
        Returns:
            str: Date formatée.
        """
        if self.created_at:
            return self.created_at.strftime("%d/%m/%Y %H:%M")
        return ""

    def formatted_updated_at(self):
        """
        Retourne la date de mise à jour formatée.
        Returns:
            str: Date formatée.
        """
        if self.updated_at:
            return self.updated_at.strftime("%d/%m/%Y %H:%M")
        return ""

class About(models.Model):
    """
    Modèle représentant la section "À propos" de l'établissement.
    """
    description = HTMLField("Description", null=True)
    mission = HTMLField("Notre mission", null=True)
    values = HTMLField("Nos valeur", null=True)
    vision = HTMLField("Notre vision", null=True)
    image = models.ImageField("photo de batiment",upload_to='about_images/', null=True)
    image_2 = models.ImageField("photo d'eleves",upload_to='about_images/', null=True)
    team  =  models.ImageField("photo d'equipe",upload_to='about_images/', null=True, blank=True)
    
    class Meta:
        db_table = 'about'
        verbose_name = 'A propo'
        
        
    def __str__(self):
        """
        Retourne le titre de la section.
        Returns:
            str: Titre de la section.
        """
        return self.description

    def formatted_created_at(self):
        """
        Retourne la date de création formatée.
        Returns:
            str: Date formatée.
        """
        if self.created_at:
            return self.created_at.strftime("%d/%m/%Y %H:%M")
        return ""

    def formatted_updated_at(self):
        """
        Retourne la date de mise à jour formatée.
        Returns:
            str: Date formatée.
        """
        if self.updated_at:
            return self.updated_at.strftime("%d/%m/%Y %H:%M")
        return ""

