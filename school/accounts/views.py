from django.shortcuts import render, get_object_or_404
from .models import Profiles
from staff.models import Staff



def login_view(request):
    pass

def profile(request, user_id):
    context={
        'profile':get_object_or_404(Profiles, user__id=user_id),
        'staff':get_object_or_404(Staff, user__id=user_id)
    }
    return render(request, "home/profiles/profile.html", context)
