from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedTabularInline
from django.utils.html import format_html
from django.db.models import Q
from django import forms
from django.core.exceptions import ValidationError

from services.utils import LANGUAGES
from services.models import *


admin.site.site_header = "🏠 Təmizxali Admin Panel"


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
    
    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if hasattr(video, 'size'):
                max_size = 120 * 1024 * 1024  # 120 MB
                if video.size > max_size:
                    raise ValidationError(
                        f'Video ölçüsü 120 MB-dan böyük ola bilməz. '
                        f'Cari ölçü: {(video.size / 1024 / 1024):.2f} MB'
                    )
        return video


class ServiceImageInline(NestedTabularInline):
    model = Image
    fk_name = 'service'
    extra = 1
    can_delete = True
    max_num = 30
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview')
    
    class Media:
        js = ('js/admin_image_compress.js',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius: 4px;" />', obj.webp_url)
        return format_html('<span style="color: #6c757d;">📷 Şəkil yoxdur</span>')
    image_preview.short_description = "🖼️ Önizləmə"


class SpecialProjectImageInline(NestedTabularInline):
    model = Image
    fk_name = 'special_project'
    extra = 1
    can_delete = True
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview')
    
    class Media:
        js = ('js/admin_image_compress.js',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius: 4px;" />', obj.webp_url)
        return format_html('<span style="color: #6c757d;">📷 Şəkil yoxdur</span>')
    image_preview.short_description = "🖼️ Önizləmə"


class AboutImageInline(NestedTabularInline):
    model = Image
    fk_name = 'about'
    extra = 1
    can_delete = True
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview')
    
    class Media:
        js = ('js/admin_image_compress.js',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius: 4px;" />', obj.webp_url)
        return format_html('<span style="color: #6c757d;">📷 Şəkil yoxdur</span>')
    image_preview.short_description = "🖼️ Önizləmə"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'get_background_pages', 'created_at')
    readonly_fields = ('image_tag', 'get_background_pages')
    
    class Media:
        js = ('js/admin_image_compress.js',)
    list_filter = (
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_calculator_page_background_image',
        'is_review_page_background_image',
        'is_testimonial_page_background_image',
        'is_projects_page_background_image',
        'created_at'
    )
    
    fieldsets = (
        ('📷 Şəkil', {
            'fields': ('image', 'image_tag')
        }),
        ('🎨 Background Şəkilləri', {
            'fields': (
                'get_background_pages',
                'is_home_page_background_image',
                'is_about_page_background_image',
                'is_calculator_page_background_image',
                'is_review_page_background_image',
                'is_testimonial_page_background_image',
                'is_projects_page_background_image',
            ),
            'description': 'Hansı səhifələr üçün background image istifadə olunacaq'
        }),
    )

    def delete_queryset(self, request, queryset):
        import logging
        logger = logging.getLogger(__name__)
        count = queryset.count()
        logger.info(f"[ADMIN BULK DELETE] Deleting {count} images...")
        
        for obj in queryset:
            obj.delete()
        
        logger.info(f"[ADMIN BULK DELETE] {count} images successfully deleted")

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.webp_url)
        return format_html('<span style="color: #6c757d;">📷 Şəkil yoxdur</span>')
    image_tag.short_description = "🖼️ Önizləmə"

    def get_background_pages(self, obj):
        """Hansı səhifələr üçün background image olduğunu göstərir"""
        pages = []
        
        if obj.is_home_page_background_image:
            pages.append(('🏠 Ana Səhifə', '#28a745'))
        if obj.is_about_page_background_image:
            pages.append(('ℹ️ Haqqımızda', '#007bff'))
        if obj.is_calculator_page_background_image:
            pages.append(('🧮 Calculator', '#17a2b8'))
        if obj.is_review_page_background_image:
            pages.append(('✍️ Rəy Əlavə Et', '#ffc107'))
        if obj.is_testimonial_page_background_image:
            pages.append(('💬 Rəylər', '#6f42c1'))
        if obj.is_projects_page_background_image:
            pages.append(('🎯 Xüsusi Layihələr', '#dc3545'))
        
        if not pages:
            return format_html('<span style="color: #6c757d; font-style: italic;">❌ Background image deyil</span>')
        
        badges = []
        for page_name, color in pages:
            badges.append(
                f'<span style="background-color: {color}; color: white; padding: 6px 12px; '
                f'border-radius: 6px; margin: 3px; font-weight: bold; font-size: 12px; display: inline-block; '
                f'box-shadow: 0 2px 4px rgba(0,0,0,0.2);">{page_name}</span>'
            )
        
        return format_html(' '.join(badges))
    get_background_pages.short_description = "📄 Hansı Səhifə üçün"



class ServiceTranslationInline(NestedTabularInline):
    model = ServiceTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = '🌐 Servis Tərcüməsi'
    verbose_name_plural = '🌐 Servis Tərcümələri'
    exclude = ['slug']
    fields = ('languages', 'name', 'description')


class ServiceVariantTranslationInline(NestedTabularInline):
    model = ServiceVariantTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = '🌐 Növ Tərcüməsi'
    verbose_name_plural = '🌐 Növ Tərcümələri'
    fields = ('languages', 'name')


@admin.register(Service)
class ServiceAdmin(NestedModelAdmin):
    form = ServiceAdminForm
    list_display = (
        'id',
        'get_service_name',
        'get_variant_prices_display',
        'measure_type',
        'get_status_badges',
        'get_media_info',
        'created_at',
    )
    list_display_links = ('id', 'get_service_name')
    list_filter = ('is_active', 'is_vip', 'is_premium', 'delivery', 'measure_type', 'created_at')
    search_fields = ('translations__name', 'translations__description')
    readonly_fields = ('created_at', 'get_status_summary', 'video_preview', 'get_variants_info')
    
    fieldsets = (
        ('📝 Əsas Məlumat', {
            'fields': ('is_active', 'measure_type', 'delivery', 'get_status_summary')
        }),
        ('💰 Qiymət Məlumatları', {
            'fields': ('get_variants_info',),
            'description': '⚠️ QEYD: Qiymətlər variantlardan götürülür. Variantlar bölməsində qiymətləri təyin edin.'
        }),
        ('⭐ Xüsusiyyətlər', {
            'fields': ('is_vip', 'is_premium'),
            'classes': ('collapse',)
        }),
        ('🎬 Media', {
            'fields': ('video', 'video_preview', 'url'),
            'description': 'Servis üçün video və ya xarici link əlavə edə bilərsiniz. ⚠️ Video ölçüsü maksimum 120 MB ola bilər.'
        }),
        ('📅 Sistem Məlumatları', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        ServiceTranslationInline,
        ServiceImageInline
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('translations', 'images', 'variants', 'variants__translations')

    def delete_queryset(self, request, queryset):
        import logging
        logger = logging.getLogger(__name__)
        count = queryset.count()
        logger.info(f"[ADMIN BULK DELETE] Deleting {count} services...")
        
        for obj in queryset:
            obj.delete()
        
        logger.info(f"[ADMIN BULK DELETE] {count} services successfully deleted")

    def get_service_name(self, obj):
        translation = obj.translations.first()
        if translation:
            return format_html(
                '<strong style="font-size: 15px; color: #007bff;">🛠️ {}</strong>',
                translation.name
            )
        return format_html('<span style="color: #6c757d;">Service #{}</span>', obj.id)
    get_service_name.short_description = '📋 Xidmət Adı'
    get_service_name.admin_order_field = 'translations__name'

    def get_variant_prices_display(self, obj):
        """Variantlardan qiymətləri göstərir"""
        try:
            variants = obj.variants.all()
            if not variants.exists():
                return format_html('<span style="color: #6c757d; font-style: italic;">⚠️ Variant yoxdur</span>')
        except Exception:
            return format_html('<span style="color: #6c757d; font-style: italic;">⚠️ Variant yoxdur</span>')
        
        prices_info = []
        for variant in variants:
            try:
                variant_name = variant.translations.first()
                name = variant_name.name if variant_name else f"Variant #{variant.id}"
            except Exception:
                name = f"Variant #{variant.id}"
            
            variant_prices = []
            if variant.price:
                variant_prices.append(
                    format_html(
                        '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                        'border-radius: 4px; font-size: 10px; margin-right: 2px;">Standart: {} AZN</span>',
                        variant.price
                    )
                )
            if variant.vip_price:
                variant_prices.append(
                    format_html(
                        '<span style="background-color: #ffc107; color: #000; padding: 3px 8px; '
                        'border-radius: 4px; font-size: 10px; margin-right: 2px;">VIP: {} AZN</span>',
                        variant.vip_price
                    )
                )
            if variant.premium_price:
                variant_prices.append(
                    format_html(
                        '<span style="background-color: #6f42c1; color: white; padding: 3px 8px; '
                        'border-radius: 4px; font-size: 10px; margin-right: 2px;">Premium: {} AZN</span>',
                        variant.premium_price
                    )
                )
            
            if variant_prices:
                prices_info.append(
                    format_html(
                        '<div style="margin-bottom: 5px;"><strong style="font-size: 11px;">{}:</strong><br>{}</div>',
                        name,
                        format_html(' '.join(variant_prices))
                    )
                )
        
        if not prices_info:
            return format_html('<span style="color: #6c757d; font-style: italic;">💰 Qiymət yoxdur</span>')
        
        return format_html(''.join(prices_info))
    get_variant_prices_display.short_description = '💰 Variant Qiymətləri'

    def get_variants_info(self, obj):
        """Variant məlumatlarını göstərir"""
        if not obj.pk:
            return format_html('<span style="color: #6c757d;">Yeni servis yaradılır - variantlar əlavə edildikdən sonra burada görünəcək</span>')
        
        try:
            variants = obj.variants.all()
            if not variants.exists():
                return format_html(
                    '<div style="background-color: #fff3cd; padding: 15px; border-radius: 6px; border-left: 4px solid #ffc107;">'
                    '<strong>⚠️ XƏBƏRDARLIQ:</strong><br>'
                    'Bu servis üçün heç bir variant yoxdur. Lütfən aşağıdakı "Servis Növləri" bölməsində variant əlavə edin və qiymətləri təyin edin.'
                    '</div>'
                )
        except Exception:
            return format_html('<span style="color: #6c757d;">⚠️ Variant məlumatları oxuna bilmədi</span>')
        
        info = []
        for variant in variants:
            try:
                variant_name = variant.translations.first()
                name = variant_name.name if variant_name else f"Variant #{variant.id}"
            except Exception:
                name = f"Variant #{variant.id}"
            
            variant_info = [f"<strong>{name}</strong>"]
            if variant.price:
                variant_info.append(f"Standart: {variant.price} AZN")
            if variant.vip_price:
                variant_info.append(f"VIP: {variant.vip_price} AZN")
            if variant.premium_price:
                variant_info.append(f"Premium: {variant.premium_price} AZN")
            
            if len(variant_info) > 1:
                info.append(' | '.join(variant_info))
        
        return format_html('<br>'.join(info))
    get_variants_info.short_description = '📦 Variant Məlumatları'

    def get_status_badges(self, obj):
        """Status badge-lərini göstərir"""
        badges = []
        
        if obj.is_active:
            badges.append(
                format_html(
                    '<span style="background-color: #28a745; color: white; padding: 4px 8px; '
                    'border-radius: 4px; font-weight: bold; font-size: 11px; margin: 2px;">✓ Aktiv</span>'
                )
            )
        else:
            badges.append(
                format_html(
                    '<span style="background-color: #dc3545; color: white; padding: 4px 8px; '
                    'border-radius: 4px; font-weight: bold; font-size: 11px; margin: 2px;">✗ Deaktiv</span>'
                )
            )
        
        if obj.is_vip:
            badges.append(
                format_html(
                    '<span style="background-color: #ffc107; color: #000; padding: 4px 8px; '
                    'border-radius: 4px; font-weight: bold; font-size: 11px; margin: 2px;">⭐ VIP</span>'
                )
            )
        
        if obj.is_premium:
            badges.append(
                format_html(
                    '<span style="background-color: #6f42c1; color: white; padding: 4px 8px; '
                    'border-radius: 4px; font-weight: bold; font-size: 11px; margin: 2px;">💎 Premium</span>'
                )
            )
        
        if obj.delivery:
            badges.append(
                format_html(
                    '<span style="background-color: #17a2b8; color: white; padding: 4px 8px; '
                    'border-radius: 4px; font-weight: bold; font-size: 11px; margin: 2px;">🚚 Çatdırılma</span>'
                )
            )
        
        return format_html(' '.join(badges))
    get_status_badges.short_description = '📊 Status'
    get_status_badges.admin_order_field = 'is_active'

    def get_media_info(self, obj):
        """Media məlumatlarını göstərir"""
        info = []
        
        if obj.video:
            info.append(
                format_html(
                    '<span style="background-color: #007bff; color: white; padding: 3px 8px; '
                    'border-radius: 4px; font-size: 11px; margin-right: 3px;">🎬 Video</span>'
                )
            )
        
        if obj.url:
            info.append(
                format_html(
                    '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; '
                    'border-radius: 4px; font-size: 11px; margin-right: 3px;">🔗 Link</span>'
                )
            )
        
        images_count = obj.images.count()
        if images_count > 0:
            info.append(
                format_html(
                    '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                    'border-radius: 4px; font-size: 11px;">📷 {} şəkil</span>',
                    images_count
                )
            )
        
        if not info:
            return format_html('<span style="color: #6c757d; font-style: italic;">📭 Media yoxdur</span>')
        
        return format_html(' '.join(info))
    get_media_info.short_description = '🎬 Media'

    def get_status_summary(self, obj):
        """Status xülasəsini göstərir"""
        if not obj.pk:
            return format_html('<span style="color: #6c757d;">🆕 Yeni servis yaradılır</span>')
        
        summary = []
        summary.append(f"🆔 ID: {obj.id}")
        
        translation = obj.translations.first()
        if translation:
            summary.append(f"📝 Ad: {translation.name}")
        
        if obj.is_active:
            summary.append("✅ Status: Aktiv")
        else:
            summary.append("❌ Status: Deaktiv")
        
        if obj.is_vip:
            summary.append("⭐ VIP")
        
        if obj.is_premium:
            summary.append("💎 Premium")
        
        try:
            variants_count = obj.variants.count()
            summary.append(f"📦 Variantlar: {variants_count}")
        except Exception:
            summary.append("📦 Variantlar: 0")
        
        return format_html('<br>'.join(summary))
    get_status_summary.short_description = '📊 Status Xülasəsi'

    def video_preview(self, obj):
        """Video preview göstərir"""
        if obj.video:
            return format_html(
                '<video width="320" height="240" controls style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
                '<source src="{}" type="video/mp4">'
                'Brauzeriniz video formatını dəstəkləmir.'
                '</video><br><a href="{}" target="_blank" style="margin-top: 10px; display: inline-block; '
                'padding: 8px 16px; background-color: #007bff; color: white; border-radius: 4px; text-decoration: none;">'
                '📥 Video yüklə</a>',
                obj.video.url,
                obj.video.url
            )
        return format_html('<span style="color: #6c757d; font-style: italic;">📭 Video yoxdur</span>')
    video_preview.short_description = '🎬 Video Önizləmə'


@admin.register(ServiceVariant)
class ServiceVariantAdmin(NestedModelAdmin):
    list_display = (
        'id',
        'get_service_name',
        'get_variant_name',
        'get_prices_display',
    )
    list_display_links = ('id', 'get_variant_name')
    list_filter = ('service', 'service__is_active')
    search_fields = ('translations__name', 'service__translations__name')
    readonly_fields = ('get_service_info', 'get_prices_summary')
    
    fieldsets = (
        ('📋 Əsas Məlumat', {
            'fields': ('service', 'get_service_info')
        }),
        ('💰 Qiymət Məlumatları', {
            'fields': ('price', 'vip_price', 'premium_price', 'get_prices_summary')
        }),
    )

    inlines = [ServiceVariantTranslationInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('service').prefetch_related('service__translations', 'translations')

    def get_service_name(self, obj):
        if obj.service:
            translation = obj.service.translations.first()
            if translation:
                return format_html(
                    '<strong style="font-size: 14px; color: #007bff;">🛠️ {}</strong>',
                    translation.name
                )
        return format_html('<span style="color: #6c757d;">❌ Servis yoxdur</span>')
    get_service_name.short_description = '🛠️ Servis'
    get_service_name.admin_order_field = 'service__translations__name'

    def get_variant_name(self, obj):
        translation = obj.translations.first()
        if translation:
            return format_html(
                '<strong style="font-size: 15px; color: #28a745;">📦 {}</strong>',
                translation.name
            )
        return format_html('<span style="color: #6c757d;">Variant #{}</span>', obj.id)
    get_variant_name.short_description = '📦 Növ Adı'
    get_variant_name.admin_order_field = 'translations__name'

    def get_prices_display(self, obj):
        """Qiymətləri göstərir"""
        prices = []
        if obj.price:
            prices.append(
                format_html(
                    '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                    'border-radius: 4px; font-size: 11px; margin-right: 2px;">Standart: {} AZN</span>',
                    obj.price
                )
            )
        if obj.vip_price:
            prices.append(
                format_html(
                    '<span style="background-color: #ffc107; color: #000; padding: 3px 8px; '
                    'border-radius: 4px; font-size: 11px; margin-right: 2px;">VIP: {} AZN</span>',
                    obj.vip_price
                )
            )
        if obj.premium_price:
            prices.append(
                format_html(
                    '<span style="background-color: #6f42c1; color: white; padding: 3px 8px; '
                    'border-radius: 4px; font-size: 11px; margin-right: 2px;">Premium: {} AZN</span>',
                    obj.premium_price
                )
            )
        
        if not prices:
            return format_html('<span style="color: #6c757d; font-style: italic;">💰 Qiymət yoxdur</span>')
        
        return format_html(' '.join(prices))
    get_prices_display.short_description = '💰 Qiymətlər'

    def get_service_info(self, obj):
        """Servis məlumatlarını göstərir"""
        if not obj.service:
            return format_html('<span style="color: #6c757d;">⚠️ Servis seçilməyib</span>')
        
        service = obj.service
        info = []
        info.append(f"🆔 Servis ID: {service.id}")
        
        translation = service.translations.first()
        if translation:
            info.append(f"📝 Servis Adı: {translation.name}")
        
        if service.is_active:
            info.append("✅ Status: Aktiv")
        else:
            info.append("❌ Status: Deaktiv")
        
        return format_html('<br>'.join(info))
    get_service_info.short_description = '📋 Servis Məlumatları'

    def get_prices_summary(self, obj):
        """Qiymət xülasəsini göstərir"""
        if not obj.pk:
            return format_html('<span style="color: #6c757d;">Yeni variant yaradılır - qiymətləri təyin edin</span>')
        
        summary = []
        summary.append(f"🆔 Variant ID: {obj.id}")
        
        translation = obj.translations.first()
        if translation:
            summary.append(f"📝 Növ Adı: {translation.name}")
        
        prices_info = []
        if obj.price:
            prices_info.append(f"Standart: {obj.price} AZN")
        if obj.vip_price:
            prices_info.append(f"VIP: {obj.vip_price} AZN")
        if obj.premium_price:
            prices_info.append(f"Premium: {obj.premium_price} AZN")
        
        if prices_info:
            summary.append("💰 Qiymətlər: " + " | ".join(prices_info))
        else:
            summary.append("💰 Qiymətlər: Təyin edilməyib")
        
        return format_html('<br>'.join(summary))
    get_prices_summary.short_description = '📊 Qiymət Xülasəsi'


class SaleEventTranslationInline(admin.TabularInline):
    model = SaleEventTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = '🌐 Endirim Tərcüməsi'
    verbose_name_plural = '🌐 Endirim Tərcümələri'


@admin.register(SaleEvent)
class SaleEventAdmin(admin.ModelAdmin):
    list_display = ('get_service_name', 'get_sale_display', 'min_quantity', 'get_active_badge')
    list_display_links = ('get_service_name',)
    list_filter = ('active', 'service')
    search_fields = ('service__translations__name',)
    inlines = [SaleEventTranslationInline]
    
    fieldsets = (
        ('📋 Əsas Məlumat', {
            'fields': ('service', 'active')
        }),
        ('💰 Endirim Məlumatları', {
            'fields': ('sale', 'min_quantity'),
            'description': 'Endirim faizi və minimum miqdar'
        }),
    )

    def get_service_name(self, obj):
        translation = obj.service.translations.first()
        if translation:
            return format_html(
                '<strong style="color: #007bff;">🛠️ {}</strong>',
                translation.name
            )
        return format_html('<span style="color: #6c757d;">-</span>')
    get_service_name.short_description = '🛠️ Servis'

    def get_sale_display(self, obj):
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 4px 10px; '
            'border-radius: 4px; font-weight: bold;">{}%</span>',
            obj.sale
        )
    get_sale_display.short_description = '💰 Endirim'

    def get_active_badge(self, obj):
        if obj.active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 4px 10px; '
                'border-radius: 4px; font-weight: bold;">✓ Aktiv</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 4px 10px; '
            'border-radius: 4px; font-weight: bold;">✗ Deaktiv</span>'
        )
    get_active_badge.short_description = '📊 Status'



class SpecialProjectTranslationInline(admin.TabularInline):
    model = SpecialProjectTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = '🌐 Xüsusi layihə tərcüməsi'
    verbose_name_plural = '🌐 Xüsusi layihə tərcümələri'


@admin.register(SpecialProject)
class SpecialProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_project_description', 'get_url_display', 'get_images_count', 'created_at')
    list_display_links = ('id', 'get_project_description')
    list_filter = ('is_active', 'created_at')
    search_fields = ('translations__description', 'url')
    inlines = [SpecialProjectTranslationInline, SpecialProjectImageInline]
    
    fieldsets = (
        ('📋 Əsas Məlumat', {
            'fields': ('is_active', 'url')
        }),
    )

    def get_project_description(self, obj):
        translation = obj.translations.first()
        if translation:
            return format_html(
                '<strong style="color: #007bff;">🎯 {}</strong>',
                translation.description[:50] + '...' if len(translation.description) > 50 else translation.description
            )
        return format_html('<span style="color: #6c757d;">-</span>')
    get_project_description.short_description = '🎯 Layihə'

    def get_url_display(self, obj):
        if obj.url:
            return format_html(
                '<a href="{}" target="_blank" style="color: #007bff;">🔗 Link</a>',
                obj.url
            )
        return format_html('<span style="color: #6c757d;">❌ Link yoxdur</span>')
    get_url_display.short_description = '🔗 URL'

    def get_images_count(self, obj):
        count = obj.images.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 4px 10px; '
                'border-radius: 4px; font-weight: bold;">📷 {} şəkil</span>',
                count
            )
        return format_html('<span style="color: #6c757d;">📷 Şəkil yoxdur</span>')
    get_images_count.short_description = '📷 Şəkillər'



class AboutTranslationInline(admin.TabularInline):
    model = AboutTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = '🌐 Haqqımızda Tərcüməsi'
    verbose_name_plural = '🌐 Haqqımızda Tərcümələri'
    
    fields = (
        'languages',
        'main_title',
        'description',
        'highlight_title_one',
        'highlight_description_one',
        'highlight_title_two',
        'highlight_description_two',
    )


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_experience_display', '__str__', 'get_images_count')
    list_display_links = ('id', '__str__')
    
    fieldsets = (
        ('📋 Əsas Məlumat', {
            'fields': ('experience_years',),
            'description': 'Xidmət etdiyiniz il sayı'
        }),
    )
    
    inlines = [AboutTranslationInline, AboutImageInline]

    def get_experience_display(self, obj):
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 6px 12px; '
            'border-radius: 6px; font-weight: bold; font-size: 14px;">⏳ {} il</span>',
            obj.experience_years
        )
    get_experience_display.short_description = '⏳ Təcrübə'

    def get_images_count(self, obj):
        count = obj.images.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 4px 10px; '
                'border-radius: 4px; font-weight: bold;">📷 {} şəkil</span>',
                count
            )
        return format_html('<span style="color: #6c757d;">📷 Şəkil yoxdur</span>')
    get_images_count.short_description = '📷 Şəkillər'



class StatisticTranslationInline(admin.TabularInline):
    model = StatisticTranslation
    extra = 1
    min_num = 1
    max_num = 10
    verbose_name = "🌐 Statistika Tərcüməsi"
    verbose_name_plural = "🌐 Statistika Tərcümələri"


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_admin_names', 'get_values_display')
    list_display_links = ('id', 'get_admin_names')
    inlines = [StatisticTranslationInline]

    def get_admin_names(self, obj):
        """Adminin daxil etdiyi translation adlarını göstərir"""
        translations = obj.translations.all()
        if translations.exists():
            names = [t.name for t in translations]
            return format_html(
                '<strong style="color: #007bff;">📊 {}</strong>',
                ', '.join(names)
            )
        return format_html('<span style="color: #6c757d;">-</span>')
    get_admin_names.short_description = "📊 Statistika Adları"

    def get_values_display(self, obj):
        """Statistika dəyərlərini göstərir"""
        translations = obj.translations.all()
        if translations.exists():
            values = []
            for t in translations:
                values.append(
                    format_html(
                        '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                        'border-radius: 4px; margin: 2px; font-weight: bold;">{}: {}</span>',
                        t.language.upper(),
                        t.value
                    )
                )
            return format_html(' '.join(values))
        return format_html('<span style="color: #6c757d;">-</span>')
    get_values_display.short_description = "🔢 Dəyərlər"



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_service_name',
        'get_fullname_display',
        'phone_number',
        'get_verified_badge',
        'created_at'
    )
    list_display_links = ('id', 'get_fullname_display')
    list_filter = ('is_verified', 'created_at', 'service')
    search_fields = ('fullname', 'phone_number', 'text', 'service__translations__name')
    
    fieldsets = (
        ('👤 Müştəri Məlumatları', {
            'fields': ('fullname', 'phone_number', 'service')
        }),
        ('💬 Rəy Məzmunu', {
            'fields': ('text',)
        }),
        ('✅ Təsdiq', {
            'fields': ('is_verified',)
        }),
        ('📅 Tarix', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)

    def get_service_name(self, obj):
        if obj.service:
            translation = obj.service.translations.first()
            if translation:
                return format_html(
                    '<strong style="color: #007bff;">🛠️ {}</strong>',
                    translation.name
                )
        return format_html('<span style="color: #6c757d;">❌ Servis yoxdur</span>')
    get_service_name.short_description = '🛠️ Servis'

    def get_fullname_display(self, obj):
        return format_html(
            '<strong style="color: #333;">👤 {}</strong>',
            obj.fullname
        )
    get_fullname_display.short_description = '👤 Ad Soyad'

    def get_verified_badge(self, obj):
        if obj.is_verified:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 4px 10px; '
                'border-radius: 4px; font-weight: bold;">✓ Təsdiqlənib</span>'
            )
        return format_html(
            '<span style="background-color: #ffc107; color: #000; padding: 4px 10px; '
            'border-radius: 4px; font-weight: bold;">⏳ Gözləyir</span>'
        )
    get_verified_badge.short_description = '✅ Status'



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_fullname_display',
        'phone_number_link',
        'is_read',
        'is_customer',
        'get_read_status',
        'get_customer_badge',
        'get_services_count',
        'created_at',
    )
    list_display_links = ('id', 'get_fullname_display')
    list_filter = ('is_read', 'is_customer', 'created_at')
    search_fields = ('fullname', 'phone_number', 'text')
    readonly_fields = ('services_badges', 'created_at', 'get_order_summary')
    list_editable = ('is_read', 'is_customer')

    fieldsets = (
        ('👤 Müştəri Məlumatları', {
            'fields': ('fullname', 'phone_number', 'text')
        }),
        ('📦 Sifariş Məlumatları', {
            'fields': ('services_badges', 'get_order_summary')
        }),
        ('📊 Status', {
            'fields': ('is_read', 'is_customer'),
        }),
        ('📅 Tarix', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_fullname_display(self, obj):
        return format_html(
            '<strong style="color: #333;">👤 {}</strong>',
            obj.fullname
        )
    get_fullname_display.short_description = '👤 Ad Soyad'

    def phone_number_link(self, obj):
        if obj.phone_number:
            return format_html(
                '<a href="{}" target="_blank" style="color: #25D366; font-weight: bold; text-decoration: none;">'
                '📱 {}</a>',
                obj.whatsapp_link(),
                obj.phone_number
            )
        return format_html('<span style="color: #6c757d;">❌ Nömrə yoxdur</span>')
    phone_number_link.short_description = "📱 Mobil Nömrə (WhatsApp)"

    def services_badges(self, obj):
        services = obj.services.all()
        if not services.exists():
            return format_html('<span style="color: #6c757d;">❌ Servis yoxdur</span>')
        
        badges = [
            format_html(
                '<span style="background-color:#5bc0de; color:white; padding:6px 12px; '
                'border-radius:6px; margin:3px; font-weight:bold; font-size:13px; display:inline-block;">'
                '🛠️ {}</span>',
                str(s)
            )
            for s in services
        ]
        return format_html(' '.join(badges))
    services_badges.short_description = "🛠️ Şifariş verilən servislər"

    def get_services_count(self, obj):
        count = obj.services.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 4px 10px; '
                'border-radius: 4px; font-weight: bold;">📦 {} servis</span>',
                count
            )
        return format_html('<span style="color: #6c757d;">❌ Servis yoxdur</span>')
    get_services_count.short_description = "📦 Servislər"

    def get_read_status(self, obj):
        """Oxunmuş/Oxunmamış statusunu göstərir"""
        if obj.is_read:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 4px 10px; '
                'border-radius: 4px; font-weight: bold; font-size: 12px;">✓ Oxunub</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 4px 10px; '
                'border-radius: 4px; font-weight: bold; font-size: 12px;">✗ Oxunmayıb</span>'
            )
    get_read_status.short_description = "📊 Status"
    get_read_status.admin_order_field = 'is_read'

    def get_customer_badge(self, obj):
        if obj.is_customer:
            return format_html(
                '<span style="background-color:#007bff; color:white; padding:4px 10px; '
                'border-radius:4px; font-weight:bold; font-size:12px;">✅ Müştəridir</span>'
            )
        else:
            return format_html(
                '<span style="background-color:#6c757d; color:white; padding:4px 10px; '
                'border-radius:4px; font-weight:bold; font-size:12px;">❌ Müştəri deyil</span>'
            )
    get_customer_badge.short_description = "👤 Müştəri"
    get_customer_badge.admin_order_field = 'is_customer'

    def get_order_summary(self, obj):
        """Sifariş xülasəsini göstərir"""
        summary = []
        summary.append(f"🆔 Sifariş ID: {obj.id}")
        summary.append(f"👤 Müştəri: {obj.fullname}")
        summary.append(f"📱 Telefon: {obj.phone_number}")
        summary.append(f"📦 Servislər: {obj.services.count()}")
        summary.append(f"📅 Tarix: {obj.created_at.strftime('%d.%m.%Y %H:%M')}")
        
        if obj.is_read:
            summary.append("✅ Status: Oxunub")
        else:
            summary.append("⏳ Status: Oxunmayıb")
        
        return format_html('<br>'.join(summary))
    get_order_summary.short_description = '📋 Sifariş Xülasəsi'



class MottoTranslationInline(admin.TabularInline):
    model = MottoTranslation
    extra = len(LANGUAGES)
    min_num = len(LANGUAGES)
    max_num = len(LANGUAGES)
    verbose_name = '🌐 Deviz Tərcüməsi'
    verbose_name_plural = '🌐 Deviz Tərcümələri'


@admin.register(Motto)
class MottoAdmin(admin.ModelAdmin):
    inlines = [MottoTranslationInline]
    list_display = ('id', 'get_motto_display')
    list_display_links = ('id', 'get_motto_display')

    def get_motto_display(self, obj):
        translation = obj.translations.first()
        if translation:
            return format_html(
                '<strong style="color: #007bff;">💭 {}</strong>',
                translation.text[:50] + '...' if len(translation.text) > 50 else translation.text
            )
        return format_html('<span style="color: #6c757d;">-</span>')
    get_motto_display.short_description = '💭 Deviz'



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_address_display',
        'get_phone_display',
        'get_whatsapp_display',
        'get_email_display',
        'get_social_count'
    )
    list_display_links = ('id', 'get_address_display')
    search_fields = ('address', 'phone', 'email', 'whatsapp_number')
    
    fieldsets = (
        ('📍 Əsas Məlumat', {
            'fields': ('address', 'phone', 'whatsapp_number', 'email')
        }),
        ('🌐 Sosial Şəbəkələr', {
            'fields': ('instagram', 'facebook', 'youtube', 'linkedn', 'tiktok'),
            'description': 'Sosial şəbəkə linkləri'
        }),
    )

    def get_address_display(self, obj):
        if obj.address:
            return format_html(
                '<strong style="color: #333;">📍 {}</strong>',
                obj.address[:40] + '...' if len(obj.address) > 40 else obj.address
            )
        return format_html('<span style="color: #6c757d;">❌ Ünvan yoxdur</span>')
    get_address_display.short_description = '📍 Ünvan'

    def get_phone_display(self, obj):
        if obj.phone:
            return format_html(
                '<span style="color: #007bff; font-weight: bold;">📞 {}</span>',
                obj.phone
            )
        return format_html('<span style="color: #6c757d;">❌ Telefon yoxdur</span>')
    get_phone_display.short_description = '📞 Telefon'

    def get_whatsapp_display(self, obj):
        if obj.whatsapp_number:
            return format_html(
                '<a href="https://wa.me/994{}" target="_blank" style="color: #25D366; font-weight: bold; text-decoration: none;">'
                '📱 {}</a>',
                obj.whatsapp_number.replace('+', '').replace(' ', ''),
                obj.whatsapp_number
            )
        return format_html('<span style="color: #6c757d;">❌ WhatsApp yoxdur</span>')
    get_whatsapp_display.short_description = '📱 WhatsApp'

    def get_email_display(self, obj):
        if obj.email:
            return format_html(
                '<a href="mailto:{}" style="color: #007bff; text-decoration: none;">📧 {}</a>',
                obj.email,
                obj.email
            )
        return format_html('<span style="color: #6c757d;">❌ Email yoxdur</span>')
    get_email_display.short_description = '📧 Email'

    def get_social_count(self, obj):
        count = sum([
            bool(obj.instagram),
            bool(obj.facebook),
            bool(obj.youtube),
            bool(obj.linkedn),
            bool(obj.tiktok)
        ])
        if count > 0:
            return format_html(
                '<span style="background-color: #6f42c1; color: white; padding: 4px 10px; '
                'border-radius: 4px; font-weight: bold;">🌐 {} sosial şəbəkə</span>',
                count
            )
        return format_html('<span style="color: #6c757d;">❌ Sosial şəbəkə yoxdur</span>')
    get_social_count.short_description = '🌐 Sosial Şəbəkələr'
