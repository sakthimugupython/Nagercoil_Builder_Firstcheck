from django.shortcuts import render
from .models import Project, ServiceImage, SiteSetting
from urllib.parse import quote_plus
import re

# Create your views here.

def home(request):
    """Home page view for Nagercoil Builders"""
    recent_projects = Project.objects.order_by('-created_at')[:3]
    return render(request, 'home.html', {'recent_projects': recent_projects})

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
    defaults = {
        'consulting': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80',
        'estimate': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80',
        'plan_design': 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&q=80',
        'construction': 'https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800&q=80',
        'flooring': 'https://images.unsplash.com/photo-1615873968403-89e068629265?w=800&q=80',
        'painting': 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=800&q=80',
        'elevation_3d': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
        'electric': 'https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=800&q=80',
        'interior_work': 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800&q=80',
        'renovation': 'https://images.unsplash.com/photo-1581858726788-75bc0f6a952d?w=800&q=80',
        'interior_design': 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&q=80',
        'carpentry': 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800&q=80',
    }
    for si in ServiceImage.objects.all():
        # Use uploaded image if present
        if si.image:
            defaults[si.key] = si.image.url
    # Build WhatsApp link for Plan & Design
    wa_link_plan = None
    settings_obj = SiteSetting.objects.order_by('-updated_at').first()
    if settings_obj and settings_obj.whatsapp_number:
        cleaned = re.sub(r'\D', '', settings_obj.whatsapp_number)
        if cleaned:
            text = settings_obj.whatsapp_template or "Hi, I'm interested in the Plan & Design service. Please share details."
            wa_link_plan = f"https://wa.me/{cleaned}?text={quote_plus(text)}"

    context = {'service_bg': defaults, 'wa_link_plan': wa_link_plan}
    return render(request, 'services.html', context)

def projects(request):
    """Projects page view for Nagercoil Builders"""
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})
