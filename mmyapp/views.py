from django.shortcuts import render

# Create your views here.

def home(request):
    """Home page view for Nagercoil Builders"""
    return render(request, 'home.html')

def about(request):
    """About page view for Nagercoil Builders"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view for Nagercoil Builders"""
    return render(request, 'contact.html')

def pricing(request):
    """Pricing page view for Nagercoil Builders"""
    return render(request, 'pricing.html')

def services(request):
    """Services page view for Nagercoil Builders"""
    return render(request, 'services.html')
