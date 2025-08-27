from django.db import models
from course.models import Course
from classes.models import Classes
from staff.models import Staff
from options.models import Options
from section.models import Section


class Courses(models.Model):  
    professor = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True, blank=True)
    course = models.ManyToManyField(Course, related_name="course")
    classe = models.ManyToManyField(Classes, related_name="classe" )
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True)
    
    
  
    
    class Meta:
        verbose_name = 'attribution cours'
        
        
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")