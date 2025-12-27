from django.urls import path

from .views.views_v1 import *


urlpatterns = [
    # Pages
    path(
        '', 
        HomePageView.as_view(), 
        name='home-page'
    ),
    path(
        'about/', 
        AboutPageView.as_view(), 
        name='about-page'
    ),
    path(
        'testimonial/',
        TestimonialPageView.as_view(),
        name='testimonial-page'
    ),
    path(
        'projects/',
        ProjectsPageView.as_view(),
        name='projects-page'
    ),
    path(
        'service/<slug:service_slug>/', 
        ServiceDetailPage.as_view(), 
        name='service-page'
    ),
    path(
        'order/',
        OrderPageView.as_view(),
        name='order-page'
    ),
    path(
        'calculator/',
        CalculatorPageView.as_view(),
        name='calculator-page'
    ),

    # Review
    path(
        'review/',
        ReviewCreateView.as_view(),
        name='create-review'
    ),

    # Projects Pagination (AJAX)
    path(
        'projects/pagination/',
        ProjectsPaginationView.as_view(),
        name='projects-pagination'
    ),
]

