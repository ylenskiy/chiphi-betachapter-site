from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def house(request):
    return render(request, 'house.html')
