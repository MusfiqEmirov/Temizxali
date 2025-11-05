from django import forms
from django.utils.translation import gettext_lazy as _

from .models.review_models import Review
from .models.order_models import Order


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
                'placeholder': _('Ad və soyadınızı daxil edin')
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Mobil nömrənizi daxil edin (məs: 501234567)')
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Rəyinizi yazın...')
            }),
        }
        
        labels = {
            'services': _('Servislər'),
            'fullname': _('Ad Soyad'),
            'phone_number': _('Mobil nömrə'),
            'text': _('Mesaj'),
        }
