from django.shortcuts import get_object_or_404
from django.views import View
from django.shortcuts import render
from django.utils import translation
from django.db.models import Prefetch


from services.models import *


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