from django.contrib import admin
from django.utils.html import format_html

from services.utils import LANGUAGES
from services.models import (
    Service, 
    ServiceTranslation, 
    SpecialProject, 
    SpecialProjectTranslation,
    Image
)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    verbose_name = 'Şəkil'
    verbose_name_plural = 'Şəkillər'
    readonly_fields = ('image_preview',)
    exclude = ('is_background_image',) 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "service":
            if hasattr(self, 'parent_model') and self.parent_model == Service:
                kwargs['queryset'] = Service.objects.filter(is_active=True)
            else:
                kwargs['queryset'] = Service.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"



class ServiceTranslationInline(admin.TabularInline):
    model = ServiceTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = 'Servis Tərcüməsi'
    verbose_name_plural = 'Servis Tərcümələri'
    exclude = ('slug',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_service_name', 'price', 'sale', 'is_active', 'is_vip', 'is_premium', 'delivery', 'created_at')
    list_display_links = ('id', 'get_service_name')
    list_filter = ('is_active', 'is_vip', 'is_premium', 'delivery', 'created_at')
    inlines = [ServiceTranslationInline, ImageInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=True)
    
    def get_service_name(self, obj):
        translation = obj.translations.first()
        if translation:
            return format_html('<strong style="font-size: 14px;">{}</strong>', translation.name)
        return '-'
    get_service_name.short_description = 'Xidmət Adı'


class SpecialProjectTranslationInline(admin.TabularInline):
    model = SpecialProjectTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = 'Xüsusi layihə tərcüməsi'
    verbose_name_plural = 'Xüsusi layihə tərcümələri'


@admin.register(SpecialProject)
class SpecialProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_project_description', 'url')
    list_display_links = ('id', 'get_project_description')
    inlines = [SpecialProjectTranslationInline, ImageInline]

    def get_project_description(self, obj):
        translation = obj.translations.first()  
        if translation:
            return format_html('<strong style="font-size: 14px;">{}</strong>', translation.description[:30])
        return '-'
    get_project_description.short_description = 'Xüsusi Layihə'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'image_tag', 'created_at')
    readonly_fields = ('image_tag',)
    fields = ('image_name', 'image', 'image_tag')  

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_tag.short_description = "Preview"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_background_image=True)

