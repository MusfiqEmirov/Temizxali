from django.urls import path
from .views.views_v1 import *

urlpatterns = [
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
]
