from django.db import models
from course.models import Course
from classes.models import Classes
from staff.models import Staff


class Courses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False, blank=False)
    classe = models.ForeignKey(Classes, on_delete=models.DO_NOTHING, null=True, blank=True)
    professor = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    class Meta:
        db_table = 'attribution de cours'
        verbose_name = 'cours attribuer'
        