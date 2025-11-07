from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator

from services.utils import SluggedModel, LANGUAGES


class Service(models.Model):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Qiymət'
    )
    vip_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='VIP Qiymət'
    )
    premium_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Premium Qiymət',
    )
    sale = models.FloatField(
        validators=[MaxValueValidator(100), MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name='Endirim'
    )
    video = models.FileField(
        upload_to='videos/',  
        null=True,
        blank=True,
        verbose_name='Video'
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Url'
    )
    is_vip = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Vip'
    )
    is_premium = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Premium'
    )
    is_number = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Ədəd ilə hesablanırsa'
    )
    is_kq = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='KQ ilə hesablanırsa'
    )
    is_kv_metr = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Kvadrat metr (m²) ilə hesablanırsa'
    )
    is_metr = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Metr (m) ilə hesablanırsa'
    )
    delivery = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Çatdırılma'
    )
    is_active = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name='Servis aktivliyi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Servis yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Servis'
        verbose_name_plural = 'Servislər'
    
    def __str__(self):
        translation = self.translations.first()
        if translation:
            return translation.name
        return f'Service #{self.id}'


class ServiceVariant(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='variants',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Servis üçün növlər'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Qiymət'
    )

    vip_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, 
        blank=True,
        verbose_name='VIP Qiymət '
    )

    premium_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, 
        blank=True,
        verbose_name='Premium Qiymət'
    )

    class Meta:
        verbose_name = 'Servis növü'
        verbose_name_plural = 'Servis növləri'

    def __str__(self):
        return f'{self.translations.name} — {self.service.translations.name}'


class ServiceTranslation(SluggedModel):
    service = models.ForeignKey(
        Service,
        related_name='translations',
        on_delete=models.CASCADE, 
        verbose_name='Servis',
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Ad'
    )
    description = models.TextField(
        validators=[MaxLengthValidator(2000)],
        verbose_name='Servis haqqında'
    )

    class Meta:
        verbose_name = 'Servis tərcüməsi'
        verbose_name_plural = 'Servis tərcümələri'
    
    def get_slug_source(self) -> str:
        return self.name

    def __str__(self):
        return f'{self.name}'


class ServiceVariantTranslation(models.Model):
    variant = models.ForeignKey(
        ServiceVariant,
        related_name='translations',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Növ'
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Növ adı'
    )

    class Meta:
        verbose_name = 'Növ ad tərcüməsi'
        verbose_name_plural = 'Növ ad tərcümələri'

    def __str__(self):
        return f'{self.name}'

    

