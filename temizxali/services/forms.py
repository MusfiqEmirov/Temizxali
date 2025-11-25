from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _, gettext

from .models.review_models import Review
from .models.order_models import Order
from services.utils import normalize_az_phone


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['services', 'fullname', 'phone_number', 'text']

        widgets = {
            'services': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input',
            }),
            'fullname': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }

        labels = {
            'services': _('Servislər'),
            'fullname': _('Ad Soyad'),
            'phone_number': _('Mobil nömrə'),
            'text': _('Mesaj'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set placeholders dynamically based on current language
        self.fields['fullname'].widget.attrs['placeholder'] = gettext('Ad və soyadınızı daxil edin')
        self.fields['phone_number'].widget.attrs['placeholder'] = gettext('Nömrənizi daxil edin (məs: 501234567)')
        self.fields['text'].widget.attrs['placeholder'] = gettext('Sifariş və ya mesajınızı buraya yazın...')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()

        if not phone:
            raise ValidationError(gettext("Mobil nömrə daxil edin."))

        normalized = normalize_az_phone(phone)

        if not normalized:
            raise ValidationError(
                gettext("Düzgün nömrə daxil edin!\n"
                "Nümunələr: 50 123 45 67 | 0501234567 | +994501234567")
            )

        # Review formasındadırsa – sifariş olub-olmadığını yoxla
        if self.__class__.__name__ == 'ReviewForm':
            if not Order.objects.filter(phone_number=normalized).exists():
                raise ValidationError(
                    gettext("Bu nömrə ilə heç bir sifariş tapılmadı. "
                    "Rəy yazmaq üçün əvvəlcə sifariş verməlisiniz")
                )

        return normalized

class ReviewForm(forms.ModelForm):
    """Rəy əlavə etmək üçün forma"""

    class Meta:
        model = Review
        fields = ['service', 'fullname', 'phone_number', 'text']

        widgets = {
            'service': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_service',
            }),
            'fullname': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_fullname',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_phone_number',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'id': 'id_text',
                'style': 'height: 120px;',
            }),
        }

        labels = {
            'service': _('Xidmət'),
            'fullname': _('Ad Soyad'),
            'phone_number': _('Mobil nömrə'),
            'text': _('Rəy'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set placeholders dynamically based on current language
        self.fields['fullname'].widget.attrs['placeholder'] = gettext('Ad və soyadınızı daxil edin')
        self.fields['phone_number'].widget.attrs['placeholder'] = gettext('Mobil nömrənizi daxil edin (məs: 501234567)')
        self.fields['text'].widget.attrs['placeholder'] = gettext('Rəyinizi yazın...')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()

        if not phone:
            raise ValidationError(gettext("Mobil nömrə daxil edin."))

        normalized = normalize_az_phone(phone)

        if not normalized:
            raise ValidationError(
                gettext("Düzgün nömrə daxil edin!\n"
                "Nümunələr: 50 123 45 67 | 0501234567 | +994501234567")
            )

        # Review formasındadırsa – sifariş olub-olmadığını yoxla
        if self.__class__.__name__ == 'ReviewForm':
            if not Order.objects.filter(phone_number=normalized).exists():
                raise ValidationError(
                    gettext("Bu nömrə ilə heç bir sifariş tapılmadı. "
                    "Rəy yazmaq üçün əvvəlcə sifariş verməlisiniz")
                )
            if Order.objects.filter(phone_number=normalized, is_customer=False):
                raise ValidationError(
                    gettext("Bu nömrə üzrə sifarişiniz hələ təsdiqlənməyib. "
                    "Rəy yazmaq üçün əvvəlcə sifarişin təsdiqlənməsini gözləməyiniz xahiş olunur.")
                )

        return normalized