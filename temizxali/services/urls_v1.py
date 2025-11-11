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
        'service/<slug:service_slug>/', 
        ServiceDetailPage.as_view(), 
        name='service-page'
    ),
    path(
        'order/',
        OrderPageView.as_view(),
        name='order-page'
    ),

    # Review
    path(
        'review/',
        ReviewCreateView.as_view(),
        name='create-review'
    ),

    # Calculator
    path(
        'calculator/', 
        ServiceCalculatorView.as_view(), 
        name='service-calculator'
    ),

    # Projects Pagination (AJAX)
    path(
        'projects/pagination/',
        ProjectsPaginationView.as_view(),
        name='projects-pagination'
    ),
]

