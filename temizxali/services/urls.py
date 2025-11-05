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
]
