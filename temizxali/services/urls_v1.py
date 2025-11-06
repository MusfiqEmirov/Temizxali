from django.urls import path

from .views.calculator_view import service_calculator
from .views.views_v1 import *


urlpatterns = [
    # HomePage
    path(
        '', 
        HomePageView.as_view(), 
        name='home-page'
    ),
    # Order
    path(
        'order/',
        OrderCreateView.as_view(),
        name='create-order'
    ),
    path(
        'order/success/',
        OrderSuccessView.as_view(),
        name='order-success'
    ),
    # Review
    path(
        'review/',
        ReviewCreateView.as_view(),
        name='create-review'
    ),
    path(
        'review/success/',
        ReviewSuccessView.as_view(),
        name='review-success'
    ),

    # Calculator
    path(
        'calculator/', 
        service_calculator, 
        name='service_calculator'
    ),
]

