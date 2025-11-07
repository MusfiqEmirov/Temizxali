from django.utils import translation
from django.conf import settings
from django.middleware.locale import LocaleMiddleware


class CustomLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            language = request.session.get('admin_language', settings.LANGUAGE_CODE)
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
        else:
            language = request.session.get('django_language')
            if language:
                translation.activate(language)
            else:
                translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = translation.get_language()
    
    def process_response(self, request, response):
        if not request.path.startswith('/admin/'):
            return super().process_response(request, response)
        return response


#test