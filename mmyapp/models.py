from django.db import models

# Create your models here.

class Project(models.Model):
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='projects/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project {self.id}"

    class Meta:
        ordering = ['order', '-created_at']


class ServiceImage(models.Model):
    KEY_CHOICES = [
        ('consulting', 'Consulting'),
        ('estimate', 'Estimate'),
        ('plan_design', 'Plan & Design'),
        ('construction', 'Construction'),
        ('flooring', 'Flooring Work'),
        ('painting', 'Painting Work'),
        ('elevation_3d', '3D Elevation Design'),
        ('electric', 'Electric Work'),
        ('interior_work', 'Interior Work'),
        ('renovation', 'Renovation'),
        ('interior_design', 'Interior Design'),
        ('carpentry', 'Carpentry Work'),
    ]

    key = models.CharField(max_length=32, choices=KEY_CHOICES, unique=True)
    image = models.ImageField(upload_to='services/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ServiceImage({self.get_key_display()})"


class SiteSetting(models.Model):
    whatsapp_number = models.CharField(max_length=32, blank=True, help_text="Include country code, e.g., 919876543210")
    whatsapp_template = models.TextField(blank=True, default="Hi, I'm interested in the Plan & Design service. Please share details.")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Settings"
