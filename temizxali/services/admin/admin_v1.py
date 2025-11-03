from django.contrib import admin
from django.utils.html import format_html
from services.models import Service, ServiceTranslation
from services.utils import LANGUAGES


class ServiceTranslationInline(admin.TabularInline):
    model = ServiceTranslation
    extra = 1
    min_num = 1
    max_num = len(LANGUAGES)
    verbose_name = 'Servis Tərcüməsi'
    verbose_name_plural = 'Servis Tərcümələri'
    exclude = ('slug',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_service_name', 'price', 'sale', 'is_active', 'is_vip', 'is_premium', 'delivery', 'created_at')
    list_display_links = ('id', 'get_service_name')
    list_filter = ('is_active', 'is_vip', 'is_premium', 'delivery', 'created_at')
    inlines = [ServiceTranslationInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=True)
    
    def get_service_name(self, obj):
        """Xidmət adını göstərir"""
        translation = obj.translations.first()
        if translation:
            return format_html('<strong style="font-size: 14px;">{}</strong>', translation.name)
        return '-'
    get_service_name.short_description = 'Xidmət Adı'

