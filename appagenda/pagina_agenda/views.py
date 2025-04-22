from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm



# Create your views here.


def index(request):
    return render(request, 'index.html')

def registrarse(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    
    return render(request, 'registrarse.html', context)

def paglogin(request):
    context = {}
    return render(request, 'login.html', context)

