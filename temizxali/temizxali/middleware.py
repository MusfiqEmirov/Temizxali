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
            # First call parent to handle standard locale detection
            super().process_request(request)
            # Then override with session language if set
            language = request.session.get('django_language')
            if language and language in dict(settings.LANGUAGES):
                translation.activate(language)
                request.LANGUAGE_CODE = translation.get_language()
    
    def process_response(self, request, response):
        if not request.path.startswith('/admin/'):
            return super().process_response(request, response)
        return response


#test