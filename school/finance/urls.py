from django.urls import path

from . import views
from .ajax_views import get_fees_for_student

app_name = 'finance'

urlpatterns = [
    path('finance/', views.index_box, name="index_finance"),

    path('finance/show/<int:student_id>/', views.show_box, name="show_box"),

    path('finance/edit_fee/<int:fee_id>/', views.edit_fee, name="edit_fee"),

    path('finance/edit_payment/<int:payment_id>/', views.edit_payment, name="edit_payment"),
    
    path('finance/add_payment/', views.add_payment, name="add_payment"),
   
    path('finance/print_receipt/<int:payment_id>/', views.print_receipt, name="print_receipt"),
    
    path('finance/fees/', views.index_fees, name="index_fees"),
    
    path('finance/fee/<int:fee_id>/', views.edit_fee, name="edit_fee"),

    path('finance/delete-fees/<int:fee_id>/', views.delete_fees, name="delete_fees"),
    
    path('finance/add_fee/', views.add_fee, name="add_fees"),
    path('finance/ajax/fees_for_student/', get_fees_for_student, name="fees_for_student"),

]
