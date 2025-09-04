
from django.urls import path
from . import views

app_name = 'finace'

urlpatterns = [
    path('', views.index_box, name="index_finance"),
    path('show<eleve_id>', views.show_box, name ="show_finace")
]
