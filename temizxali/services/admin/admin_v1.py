from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedTabularInline
from django.utils.html import format_html

from services.utils import LANGUAGES
from services.models import *


# Image Admin
class ServiceImageInline(NestedTabularInline):
    model = Image
    fk_name = 'service'
    extra = 1
    readonly_fields = ('image_preview',)
    fields = ('image_name', 'image', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


class SpecialProjectImageInline(NestedTabularInline):
    model = Image
    fk_name = 'special_project'
    extra = 6
    readonly_fields = ('image_preview',)
    fields = ('image_name', 'image', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'image_tag', 'created_at',)
    readonly_fields = ('image_tag',)
    fields = ('image_name', 'image', 'image_tag', 'is_background_image')  

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_tag.short_description = "Preview"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_background_image=True)

# Service Admin
class ServiceTranslationInline(NestedTabularInline):
    model = ServiceTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = 'Servis Tərcüməsi'
    verbose_name_plural = 'Servis Tərcümələri'
    exclude = ['slug']


class ServiceVariantTranslationInline(NestedTabularInline):
    model = ServiceVariantTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = 'Növ Tərcüməsi'
    verbose_name_plural = 'Növ Tərcümələri'


class ServiceVariantInline(NestedTabularInline):
    model = ServiceVariant
    extra = 1
    verbose_name = 'Servis Növü'
    verbose_name_plural = 'Servis Növləri'
    inlines = [ServiceVariantTranslationInline]

@admin.register(Service)
class ServiceAdmin(NestedModelAdmin):
    list_display = (
        'id', 'get_service_name', 'price', 'vip_price', 'measure_type',
        'premium_price', 'is_active', 'delivery', 'created_at', 
        
    )
    list_display_links = ('id', 'get_service_name')
    list_filter = ('is_active', 'delivery', 'created_at')

    inlines = [
        ServiceTranslationInline,
        ServiceVariantInline,
        ServiceImageInline
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=True)

    def get_service_name(self, obj):
        translation = obj.translations.first()
        if translation:
            return format_html('<strong style="font-size: 14px;">{}</strong>', translation.name)
        return '-'
    get_service_name.short_description = 'Xidmət Adı'


# #Sale Events
class SaleEventTranslationInline(admin.TabularInline):
    model = SaleEventTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)


@admin.register(SaleEvent)
class SaleEventAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'sale', 'min_quantity', 'active')
    list_filter = ('service', 'active')
    search_fields = ('service__translations__name',)
    inlines = [SaleEventTranslationInline]

    def service_name(self, obj):
        return obj.service.translations.first().name
    
    service_name.short_description = 'Servis'


# SpecialProject Admin
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
    inlines = [SpecialProjectTranslationInline, SpecialProjectImageInline]

    def get_project_description(self, obj):
        translation = obj.translations.first()  
        if translation:
            return format_html('<strong style="font-size: 14px;">{}</strong>', translation.description[:30])
        return '-'
      
    get_project_description.short_description = 'Xüsusi Layihə'


# About Admin
class AboutTranslationInline(admin.TabularInline):
    model = AboutTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = 'Haqqımızda Tərcüməsi'
    verbose_name_plural = 'Haqqımızda Tərcümələri'


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutTranslationInline]
    list_display = ['id', '__str__']


# Statistics Admin
@admin.register(Statistic)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client_count',
        'work_done_count',
        'staff_count',
        'achievement_count',
    )
    list_display_links = ('id',)


# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'fullname', 'phone_number', 'is_verified', 'created_at')
    list_display_links = ('id', 'fullname')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('fullname', 'phone_number', 'comment') 
 

 # Order Admin 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number_link', 'created_at', 'get_services')
    list_display_links = ('id', 'fullname')
    list_filter = ('created_at',)
    search_fields = ('fullname', 'phone_number', 'text')
    readonly_fields = ('services_badges', 'created_at') 

    fieldsets = (
        (None, {
            'fields': ('fullname', 'phone_number', 'text', 'services_badges')
        }),
        ('Əlavə məlumat', {
            'fields': ('created_at',),
        }),
    )

    def phone_number_link(self, obj):
        if obj.phone_number:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.whatsapp_link(),
                obj.phone_number
            )
        return "-"
    phone_number_link.short_description = "Mobil Nömrə (WhatsApp)"

    def services_badges(self, obj):
        badges = [
            f'<span style="background-color:#5bc0de; color:white; padding:4px 10px; border-radius:6px; margin:2px; font-weight:bold; font-size:14px;">{str(s)}</span>'
            for s in obj.services.all()
        ]
        return format_html(" ".join(badges))
    services_badges.short_description = "Şifariş verilən servislər"

    def get_services(self, obj):
        badges = [
            f'<span style="background-color:#5bc0de; color:white; padding:2px 6px; border-radius:4px; margin:1px;">{str(s)}</span>'
            for s in obj.services.all()
        ]
        return format_html(" ".join(badges))
    get_services.short_description = "Servislər"

    

# Motto Admin
class MottoTranslationInline(admin.TabularInline):
    model = MottoTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = 'Deviz Tərcüməsi'
    verbose_name_plural = 'Deviz Tərcümələri'


@admin.register(Motto)
class MottoAdmin(admin.ModelAdmin):
    inlines = [MottoTranslationInline]
    list_display = ['id', '__str__']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'phone', 'email')
    search_fields = ('address', 'phone', 'email')
    list_display_links = ('id', 'address')
    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Sosial Şəbəkələr', {
            'fields': ('instagram', 'facebook', 'youtube', 'linkedn', 'tiktok')
        }),
    )