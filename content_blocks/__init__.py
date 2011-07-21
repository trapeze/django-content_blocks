from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


REQUIRED_APPS = (
    'django.contrib.markup',
    'django.contrib.webdesign',
    'linguo',
)


if __name__ in settings.INSTALLED_APPS:
    for application_name in REQUIRED_APPS:
        if not application_name in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("%s application requires %s. "
            "Please ensure this is included in your INSTALLED_APPS." % (
                __name__,
                application_name,
            ))

    try:
        import markdown
    except ImportError:
        raise ImproperlyConfigured("%s application requires markdown. "
        "Please install it in your path (for example, as ../lib/markdown.py)" % (
            __name__,
        ))
