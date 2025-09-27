from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('doyen/', views.dean, name='dean'),
    path("staff/", views.staff, name='staff'),
]