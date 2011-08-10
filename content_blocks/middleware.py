from django.conf import settings
from django.utils import translation

class ForceEnglishInAdminMiddleware(object):
    # Content blocks breaks if admin is any other language than LANGUAGE_CODE
    # (typically en). Force to English. See #001011-630 for more details.
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__module__.startswith('django.contrib.admin.'):
            translation.activate(settings.LANGUAGE_CODE)
        return None
