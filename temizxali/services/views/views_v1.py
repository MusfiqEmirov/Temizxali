
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.db.models import Prefetch

from services.models import *
from services.forms import OrderForm
from services.forms import ReviewForm


__all__ = [
    'HomePageView'
    'OrderCreateView',
    'OrderSuccessView',
    'ReviewCreateView',
    'ReviewSuccessView',
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
    

class ReviewCreateView(View):
    """Rəy əlavə etmək üçün səhifə"""
    template_name = 'review_form.html'

    def get(self, request):
        """Formu göstərir"""
        form = ReviewForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ReviewForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data.get('phone_number')
            if Order.objects.filter(phone_number=phone).exists():
                form.save()
                messages.success(request, "Rəyiniz uğurla göndərildi ✅")
                return redirect('review-success')
            else:
                messages.error(
                    request,
                    "Bu nömrə ilə verilmiş sifariş tapılmadı. Rəy yazmaq üçün əvvəlcə sifariş verməlisiniz ❌"
                )
        else:
            messages.error(request, "Zəhmət olmasa formu düzgün doldurun ❌")

        return render(request, self.template_name, {'form': form})


class ReviewSuccessView(View):
    template_name = 'review_success.html'

    def get(self, request):
        return render(request, self.template_name)





class HomePageView(View):
    def get(self, request):
        languages = translation.get_language()

        background_image = Image.objects.filter(
            image_name='home_page_background', 
            is_background_image=True
        ).first()
        services = Service.objects.filter(
            is_active=True,
            translations__languages = languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=languages)),
            'images'
        )
        special_projects = SpecialProject.objects.filter(
            is_active=True,
            translations__languages = languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=SpecialProjectTranslation.objects.filter(languages=languages)),
            'images'
        )
        statistics = Statistic.objects.all()
        reviews = Review.objects.filter(is_verified=True)

        return render(request, 'home_page.html', {
            'background_image': background_image,
            'services': services,
            'special_projects': special_projects,
            'statistics': statistics,
            'reviews': reviews
            })

