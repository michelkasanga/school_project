
from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('', views.index, name="index")
]
