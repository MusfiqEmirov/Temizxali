from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from services.forms import OrderForm

__all__ = [
    'OrderCreateView',
    'OrderSuccessView'
]

class OrderCreateView(View):
    
    template_name = 'order_form.html'
    
    def get(self, request):
        form = OrderForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sifarişiniz uğurla göndərildi")
            return redirect("order-success")
        else:
            messages.error(request, "Zəhmət olmasa formu düzgün doldurun ")
            return render(request, self.template_name, {'form': form})
    


class OrderSuccessView(View):
    template_name = 'order_success.html'

    def get(self, request):
        """Sifarişin uğurla göndərildiyi səhifə"""
        return render(request, self.template_name)
