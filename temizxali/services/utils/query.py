from django.db.models import Prefetch
from django.utils import translation
from django.conf import settings


class CalculatorQuery:
    """
    Utility class responsible for loading services and their translations
    based on the current active language.
    """
    @staticmethod
    def load_services():
        """
        Load all active services with language-specific translations.

        Returns:
            QuerySet: A queryset of `Service` objects prefetching translations
                      and variant translations filtered by current language.
        """
        # Lazy import to avoid circular import
        from services.models import Service, ServiceTranslation, ServiceVariant, ServiceVariantTranslation
        
        lang = translation.get_language()
        return (
            Service.objects.filter(
                is_active=True,
                translations__languages=lang,
            )
            .distinct()
            .prefetch_related(
                Prefetch(
                    'translations',
                    queryset=ServiceTranslation.objects.filter(languages=lang),
                ),
                Prefetch(
                    'variants',
                    queryset=ServiceVariant.objects.all().prefetch_related(
                        Prefetch(
                            'translations',
                            queryset=ServiceVariantTranslation.objects.filter(languages=lang),
                        )
                    ),
                ),
            )
        )