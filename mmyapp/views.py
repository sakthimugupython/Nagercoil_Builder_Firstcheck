from django.shortcuts import render
from .models import Project, ServiceImage, SiteSetting
from urllib.parse import quote
import re


class _SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def _render_template(template, fallback, **kwargs):
    template = template.strip() if template else ''
    if template:
        try:
            rendered = template.format_map(_SafeDict(kwargs))
            if rendered.strip():
                return rendered
        except (KeyError, ValueError):
            pass
    return fallback


def _apply_template(message_template, fallback, **kwargs):
    template = (message_template or '').strip()
    if not template:
        return fallback
    if '{' in template and '}' in template:
        return _render_template(template, fallback, **kwargs)
    # Treat template as prefix without dynamic placeholders
    return f"{template}\n\n{fallback}".strip()


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
    context = {}
    settings_obj = SiteSetting.objects.order_by('-updated_at').first()
    if settings_obj and settings_obj.whatsapp_number:
        cleaned = re.sub(r'\D', '', settings_obj.whatsapp_number)
        if cleaned:
            message_template = settings_obj.whatsapp_template or ''
            package_details = {
                'basic': {
                    'name': 'Basic Package',
                    'price': '₹1600 per sq ft',
                    'features': [
                        '2D Plan',
                        'Country Brick & M Sand',
                        'Shankar Cement & 550 D TMT',
                        'Tiles @ ₹40/sq ft',
                    ],
                    'description': 'Entry-level construction package with reliable materials and essential finishes.',
                },
                'standard': {
                    'name': 'Standard Package',
                    'price': '₹2000 per sq ft',
                    'features': [
                        '2D + 3D Plan',
                        'Pillar foundation (load bearing)',
                        'Country Brick & M Sand',
                        'Tiles: Wall ₹40 / Floor ₹60',
                    ],
                    'description': 'Balanced package combining structural strength with upgraded finishes for most homes.',
                },
                'premium': {
                    'name': 'Premium Package',
                    'price': '₹2500 per sq ft',
                    'features': [
                        '2D + 3D Plan',
                        'Pillar foundation (load bearing)',
                        'Champour Brick & M Sand',
                        'Granite flooring',
                    ],
                    'description': 'High-end specification focused on premium materials and finishes throughout the build.',
                },
            }
            package_messages = {
                key: _apply_template(
                    message_template,
                    fallback=(
                        f"Hi! I'm interested in the {detail['name']} ({detail['price']}). "
                        f"{detail.get('description', '').strip()}\n"
                        f"Highlights:\n{chr(10).join(f'- {feat}' for feat in detail.get('features', []))}"
                    ).strip(),
                    package=detail['name'],
                    service=detail['name'],
                    package_name=detail['name'],
                    service_name=detail['name'],
                    plan=detail['name'],
                    plan_name=detail['name'],
                    price=detail['price'],
                    package_price=detail['price'],
                    service_price=detail['price'],
                    price_per_sqft=detail['price'],
                    amount=detail['price'],
                    description=detail.get('description', ''),
                    summary=detail.get('description', ''),
                    features=', '.join(detail.get('features', [])),
                    features_list='\n'.join(detail.get('features', [])),
                    highlights=', '.join(detail.get('features', [])),
                    highlights_list='\n'.join(detail.get('features', [])),
                    category='package',
                    slug=key,
                )
                for key, detail in package_details.items()
            }
            context['wa_links'] = {
                key: f"https://wa.me/{cleaned}?text={quote(message.strip())}"
                for key, message in package_messages.items()
            }

    return render(request, 'pricing.html', context)

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
    service_titles = {
        'consulting': 'Consulting',
        'estimate': 'Estimate',
        'plan_design': 'Plan & Design',
        'construction': 'Construction',
        'flooring': 'Flooring Work',
        'painting': 'Painting Work',
        'elevation_3d': '3D Elevation Design',
        'electric': 'Electric Work',
        'interior_work': 'Interior Work',
        'renovation': 'Renovation',
        'interior_design': 'Interior Design',
        'carpentry': 'Carpentry Work',
    }
    service_details = {
        'consulting': {
            'description': 'Expert guidance to assess challenges, plan strategy, and reduce risks throughout the project.',
            'highlights': ['Requirement analysis', 'Budget & timeline planning', 'Risk mitigation insights'],
        },
        'estimate': {
            'description': 'Transparent cost, material, and schedule estimations to help you plan effectively.',
            'highlights': ['Detailed BOQ', 'Cost breakdown options', 'Indicative schedules'],
        },
        'plan_design': {
            'description': 'Architectural planning with drawings and 3D models to translate ideas into build-ready designs.',
            'highlights': ['2D/3D drawings', 'Space planning', 'Material and finish schedules'],
        },
        'construction': {
            'description': 'End-to-end site execution with quality control across structural, masonry, and finishing works.',
            'highlights': ['Structural execution', 'Site supervision', 'Schedule tracking'],
        },
        'flooring': {
            'description': 'Installation of premium tile, granite, wooden, and vinyl flooring with precision finishing.',
            'highlights': ['Subfloor prep', 'Precision laying', 'Polishing & sealing'],
        },
        'painting': {
            'description': 'Interior and exterior painting with surface prep, putty, primer, and durable finishes.',
            'highlights': ['Surface prep & repairs', 'Putty & primer', 'Premium finish coats'],
        },
        'elevation_3d': {
            'description': 'Photorealistic exterior visualisations with materials, lighting, and landscape options.',
            'highlights': ['Rendering previews', 'Multiple material palettes', 'Lighting options'],
        },
        'electric': {
            'description': 'Electrical wiring, panels, lighting, and safety-compliant systems for homes and commercial spaces.',
            'highlights': ['New wiring / rewiring', 'DB & earthing setup', 'Lighting installations'],
        },
        'interior_work': {
            'description': 'Turnkey interior execution including ceilings, partitions, cabinetry, and lighting integration.',
            'highlights': ['False ceilings & partitions', 'Modular cabinetry', 'Lighting integration'],
        },
        'renovation': {
            'description': 'Upgrades and transformations for existing spaces covering structure, plumbing, and finishes.',
            'highlights': ['Layout improvements', 'Kitchen/bath upgrades', 'Waterproofing & repairs'],
        },
        'interior_design': {
            'description': 'Space planning, material selection, and decor curation for balanced, beautiful interiors.',
            'highlights': ['Concept boards', 'Furniture layouts', 'Material & color palettes'],
        },
        'carpentry': {
            'description': 'Custom cabinetry, doors, frames, and on-site joinery with durable materials and finishes.',
            'highlights': ['Custom wardrobes', 'Door & frame fabrication', 'Finishing & polish'],
        },
    }
    for si in ServiceImage.objects.all():
        # Use uploaded image if present
        if si.image:
            defaults[si.key] = si.image.url
    wa_links = {}
    settings_obj = SiteSetting.objects.order_by('-updated_at').first()
    if settings_obj and settings_obj.whatsapp_number:
        cleaned = re.sub(r'\D', '', settings_obj.whatsapp_number)
        if cleaned:
            message_template = settings_obj.whatsapp_template or ''
            service_messages = {}
            for key, title in service_titles.items():
                service_detail = service_details.get(key, {})
                highlights_lines = '\n'.join(f"- {item}" for item in service_detail.get('highlights', []))
                description = service_detail.get('description', '')
                fallback = (
                    f"Hi! I'd like to know more about your {title} service. "
                    f"{description.strip()}\n"
                    f"Key points:\n{highlights_lines}"
                ).strip()
                service_messages[key] = _apply_template(
                    message_template,
                    fallback=fallback,
                    service=title,
                    package=title,
                    service_name=title,
                    package_name=title,
                    plan=title,
                    plan_name=title,
                    price='',
                    service_price='',
                    package_price='',
                    price_per_sqft='',
                    amount='',
                    description=service_details.get(key, {}).get('description', ''),
                    summary=service_details.get(key, {}).get('description', ''),
                    highlights=', '.join(service_details.get(key, {}).get('highlights', [])),
                    highlights_list='\n'.join(service_details.get(key, {}).get('highlights', [])),
                    features=', '.join(service_details.get(key, {}).get('highlights', [])),
                    features_list='\n'.join(service_details.get(key, {}).get('highlights', [])),
                    category='service',
                    slug=key,
                )

            wa_links = {
                key: f"https://wa.me/{cleaned}?text={quote(message.strip())}"
                for key, message in service_messages.items()
            }

    context = {'service_bg': defaults, 'wa_links': wa_links}
    return render(request, 'services.html', context)

def projects(request):
    """Projects page view for Nagercoil Builders"""
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})
