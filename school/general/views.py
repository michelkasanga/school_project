from django.shortcuts import render

def index(request):
    context = {
        'salut': 'salut'
    }
    return render(request, 'home/index.html', context)