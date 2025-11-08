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
    extra = 1
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
        'id', 'get_service_name', 'price', 'vip_price', 'is_number', 'is_kq', 'is_kv_metr', 'is_metr',
        'premium_price', 'sale', 'is_active', 'delivery', 'created_at', 
        
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
    list_display = ('id', 'fullname', 'phone_number', 'is_verified', 'created_at')
    list_display_links = ('id', 'fullname')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('fullname', 'phone_number', 'comment') 
 

 # Order Admin 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'created_at')
    list_display_links = ('id', 'fullname')
    list_filter = ('created_at',)
    search_fields = ('fullname', 'phone_number', 'text')
    filter_horizontal = ('services',) 


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
    list_display = ('id', 'address', 'phone', 'phone_second', 'email', 'email_second')
    search_fields = ('address', 'phone', 'phone_second', 'email', 'email_second')
    list_display_links = ('id', 'address')
    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('address', 'phone', 'phone_second', 'email', 'email_second')
        }),
        ('Sosial Şəbəkələr', {
            'fields': ('social_one', 'social_two', 'social_three')
        }),
    )