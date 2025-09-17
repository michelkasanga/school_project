
from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('', views.index, name="index"), 
    path('notfoud/', views.event_404),
    path('about/', views.about, name='about'),
    path('event/', views.event, name='event'),
    path('/<str:cat>', views.category_event, name='category_event'),
    path("event/<int:id>", views.show_event, name='show_event'),
    path('program/', views.program,  name='program'),
    path('program/<int:id>', views.program_view, name='show_program'),
]
