from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('profile/<int:user_id>/',views.profile ,name="profile"),
    path('students/<int:user_id>/',views.profile_students ,name="profile_students"),
    path('profile/edit/<int:user_id>/',views.edit_profile ,name="edit_profile"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout")
    
]
    
