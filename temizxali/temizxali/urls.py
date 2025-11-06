from django.contrib import admin
from django.urls import path, include
from django.conf import settings            
from django.conf.urls.static import static 
from services.views.i18n_views import set_language


urlpatterns = [
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),
    path('i18n/setlang/', set_language, name='set_language'),
    path('', include('services.urls_v1'))
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
