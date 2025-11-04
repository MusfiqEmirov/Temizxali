from django.contrib import admin
from django.utils.html import format_html

from services.utils import LANGUAGES
from services.models import (
    Service, 
    ServiceTranslation, 
    SpecialProject, 
    SpecialProjectTranslation,
    Image,
    About,
    AboutTranslation,
    Statistics,
    Review,
    Order
)

# Image Admin
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
    inlines = [SpecialProjectTranslationInline, ImageInline]

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
@admin.register(Statistics)
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
    filter_horizontal = ('services',)  
 

 # Order Admin 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'created_at')
    list_display_links = ('id', 'fullname')
    list_filter = ('created_at',)
    search_fields = ('fullname', 'phone_number', 'text')
    filter_horizontal = ('services',) 