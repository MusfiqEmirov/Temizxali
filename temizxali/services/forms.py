from django import forms
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
                'placeholder': 'Ad və soyadınızı daxil edin',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nömrənizi daxil edin (məs: 501234567)',
                'maxlength': '10',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Sifariş və ya mesajınızı buraya yazın...',
            }),
        }

        labels = {
            'services': 'Servislər',
            'fullname': 'Ad Soyad',
            'phone_number': 'Mobil nömrə',
            'text': 'Mesaj',
        }
