from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models.review_models import Review
from .models.order_models import Order
from services.utils.normalize_phone_number import normalize_az_phone


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



class ReviewForm(forms.ModelForm):
    """Rəy əlavə etmək üçün forma"""

    class Meta:
        model = Review
        fields = ['services', 'fullname', 'phone_number', 'text']

        widgets = {
            'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'fullname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Ad və soyadınızı daxil edin'),
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Mobil nömrənizi daxil edin (məs: 501234567)'),
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Rəyinizi yazın...'),
            }),
        }

        labels = {
            'services': _('Servislər'),
            'fullname': _('Ad Soyad'),
            'phone_number': _('Mobil nömrə'),
            'text': _('Mesaj'),
        }

    def clean_phone_number(self):
        """Nömrəni formatlayır və sifarişlə uyğunluğunu yoxlayır."""
        phone = self.cleaned_data.get('phone_number')

        if not phone:
            return phone

        normalized_phone = normalize_az_phone(phone)

        # Əgər belə nömrə ilə sifariş yoxdursa — xətanı qaytar
        if not Order.objects.filter(phone_number=normalized_phone).exists():
            raise ValidationError(
                _("Bu nömrə ilə verilmiş sifariş tapılmadı. Rəy yazmaq üçün əvvəlcə sifariş verməlisiniz ❌")
            )

        # Əks halda təmizlənmiş nömrəni qaytar
        return normalized_phone