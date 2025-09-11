
from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('finance/', views.index_box, name="index_finance"),
    path('show/<int:eleve_id>/', views.show_box, name ="show_finance")
]
