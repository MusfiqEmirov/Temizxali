from django.urls import path
from .views.views_v1 import *


urlpatterns = [
    path(
        '', 
        HomePageView.as_view(), 
        name='home-page'
    ),
]