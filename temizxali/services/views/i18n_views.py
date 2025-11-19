from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.http import require_POST
from django.conf import settings

@require_POST
def set_language(request):
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    admin_path = f'/{settings.ADMIN_URL.strip("/")}/'
    is_admin = next_url.startswith(admin_path)

    language = request.POST.get('language') or request.GET.get('language')

    if language and language in dict(settings.LANGUAGES):
        if is_admin:
            # Admin panel dili həmişə az qalacaq
            request.session['admin_language'] = settings.LANGUAGE_CODE
        else:
            request.session['django_language'] = language
            translation.activate(language)

    return HttpResponseRedirect(next_url)
