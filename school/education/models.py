"""
Modèles pour la gestion de la structure pédagogique (sections, options, classes, cours, titulaires, etc.).
Chaque classe et méthode est documentée selon les standards Pylint.
"""

from django.db import models
from staff.models import Staff

  
class Section(models.Model):
    """
    Modèle représentant une section pédagogique (ex : scientifique, littéraire).
    """
    name = models.CharField('Nom du section',max_length=100, unique=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='section'
        verbose_name = 'section'
        verbose_name_plural = 'sections'
        ordering = ['name']  
    
    def __str__(self):
        """
        Retourne le nom de la section.
        Returns:
            str: Nom de la section.
        """
        return self.name
    
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
    
    
#_______________________________________________________
class Options(models.Model):
    """
    Modèle représentant une option pédagogique (ex : math, biochimie, latin).
    """
    name = models.CharField("Nom d'option",max_length=100, unique=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='options'
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
        ordering = ['name']  
    
    def __str__(self):
        """
        Retourne le nom de l'option.
        Returns:
            str: Nom de l'option.
        """
        return self.name
    
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
    

#__________________________________________________

class Course(models.Model):
    """
    Modèle représentant un cours enseigné dans l'établissement.
    """
    name = models.CharField("Nom du Cours",max_length= 255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='course'
        verbose_name = 'cours'
        verbose_name_plural = 'cours'
        ordering = ['name']
        
    def __str__(self):
        """
        Retourne le nom du cours.
        Returns:
            str: Nom du cours.
        """
        return self.name
    
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

#____________________________________________________


class Classes(models.Model):
    """
    Modèle représentant une classe scolaire (ex : 6ème, 5ème, terminale).
    """
    name = models.CharField("Classe",max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='classes'
        verbose_name = 'classe'
        verbose_name_plural = 'classes'
        ordering = ['name']
        
    def __str__(self):
        """
        Retourne le nom de la classe.
        Returns:
            str: Nom de la classe.
        """
        return self.name
    
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
    

class Tutors(models.Model):
    """
    Modèle représentant un titulaire de classe (professeur principal).
    """
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.SET_NULL, null= True, blank=True)
    
    class Meta:
        db_table='tutors'
        verbose_name = 'Titulaire'
        verbose_name_plural = 'Titulaires'
  
  
#___________________________________________________
class Courses(models.Model):  
    professor = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True, blank=True)
    course = models.ManyToManyField(Course, related_name="course")
    classe = models.ManyToManyField(Classes, related_name="classe" )
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='courses'
        verbose_name = 'attribution cours'
           
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
