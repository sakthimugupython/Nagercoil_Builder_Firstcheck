from django.contrib import admin
from .models import Project, ServiceImage, SiteSetting

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "created_at")
    list_editable = ("order",)
    ordering = ("order", "-created_at")

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ("key", "updated_at")
    list_filter = ("key",)

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("whatsapp_number", "updated_at")
