from django.utils import translation
from django.conf import settings
from django.middleware.locale import LocaleMiddleware


class CustomLocaleMiddleware(LocaleMiddleware):
    def is_admin_path(self, path):
        admin_url = settings.ADMIN_URL.rstrip('/')
        if not admin_url.startswith('/'):
            admin_url = '/' + admin_url
        return path.startswith(admin_url)
    
    def process_request(self, request):
        if self.is_admin_path(request.path):
            translation.deactivate_all()
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
            request.session['django_language'] = settings.LANGUAGE_CODE
        else:
            super().process_request(request)
            language = request.session.get('django_language')
            if language and language in dict(settings.LANGUAGES):
                translation.activate(language)
                request.LANGUAGE_CODE = translation.get_language()
    
    def process_response(self, request, response):
        if self.is_admin_path(request.path):
            if hasattr(response, 'set_cookie'):
                cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
                cookie_age = getattr(settings, 'LANGUAGE_COOKIE_AGE', None)
                cookie_path = getattr(settings, 'LANGUAGE_COOKIE_PATH', '/')
                cookie_domain = getattr(settings, 'LANGUAGE_COOKIE_DOMAIN', None)
                response.set_cookie(
                    cookie_name,
                    settings.LANGUAGE_CODE,
                    max_age=cookie_age,
                    path=cookie_path,
                    domain=cookie_domain,
                )
            return response
        return super().process_response(request, response)