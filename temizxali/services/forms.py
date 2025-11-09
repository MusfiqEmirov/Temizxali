from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
                'placeholder': _('Ad və soyadınızı daxil edin'),
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nömrənizi daxil edin (məs: 501234567)'),
                'maxlength': '10',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Sifariş və ya mesajınızı buraya yazın...'),
            }),
        }

        labels = {
            'services': _('Servislər'),
            'fullname': _('Ad Soyad'),
            'phone_number': _('Mobil nömrə'),
            'text': _('Mesaj'),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()

        if not phone:
            raise ValidationError("Mobil nömrə daxil edin.")

        normalized = normalize_az_phone(phone)

        if not normalized:
            raise ValidationError(
                "Düzgün nömrə daxil edin!\n"
                "Nümunələr: 50 123 45 67 | 0501234567 | +994501234567"
            )

        # Review formasındadırsa – sifariş olub-olmadığını yoxla
        if self.__class__.__name__ == 'ReviewForm':
            if not Order.objects.filter(phone_number=normalized).exists():
                raise ValidationError(
                    "Bu nömrə ilə heç bir sifariş tapılmadı. "
                    "Rəy yazmaq üçün əvvəlcə sifariş verməlisiniz"
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
                'placeholder': _('Ad və soyadınızı daxil edin'),
                'id': 'id_fullname',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Mobil nömrənizi daxil edin (məs: 501234567)'),
                'id': 'id_phone_number',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Rəyinizi yazın...'),
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

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()

        if not phone:
            raise ValidationError("Mobil nömrə daxil edin.")

        normalized = normalize_az_phone(phone)

        if not normalized:
            raise ValidationError(
                "Düzgün nömrə daxil edin!\n"
                "Nümunələr: 50 123 45 67 | 0501234567 | +994501234567"
            )

        # Review formasındadırsa – sifariş olub-olmadığını yoxla
        if self.__class__.__name__ == 'ReviewForm':
            if not Order.objects.filter(phone_number=normalized).exists():
                raise ValidationError(
                    "Bu nömrə ilə heç bir sifariş tapılmadı. "
                    "Rəy yazmaq üçün əvvəlcə sifariş verməlisiniz"
                )

        return normalized