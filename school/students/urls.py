from django.urls import path
from . import views

urlpatterns = [
    path('liste/', views.students_list, name='students_list'),
]
