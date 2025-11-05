from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.http import require_POST
from django.conf import settings


@require_POST
def set_language(request):
    next_url = request.POST.get('next', request.GET.get('next'))
    if not next_url:
        next_url = request.META.get('HTTP_REFERER', '/')
        if not next_url:
            next_url = '/'
    
    is_admin = next_url.startswith('/admin/') if next_url else False
    language = request.POST.get('language', request.GET.get('language'))
    
    if language and language in dict(settings.LANGUAGES):
        if is_admin:
            request.session['admin_language'] = language
            translation.activate(language)
        else:
            request.session['django_language'] = language
            translation.activate(language)
    
    return HttpResponseRedirect(next_url)

