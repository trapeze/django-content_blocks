from django import template
from django.conf import settings

from content_blocks.forms import ContentBlockForm
from content_blocks.models import ContentBlock


register = template.Library()


@register.inclusion_tag("content_blocks/block.html", takes_context=True)
def show_content_block(context, name, editable=True, markup=True):
    """
    Renders the block with the given name and the context language
    If there block has no content and DEBUG is true, renders lorem ipsum text
    """
    try:
        block = ContentBlock.objects.get(
            core__name=name,
            language=context.get("LANGUAGE_CODE", None)
        )
    except ContentBlock.DoesNotExist:
        block = None

    return {
        "name": name,
        "block": block,
        "editable": (editable is True or editable == "True"),
        "markup": (markup is True or markup == "True"),
        "perms": context.get("perms", None),
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE", None),
        "MEDIA_URL": context.get("MEDIA_URL", None),
        "DEBUG": settings.DEBUG,
    }


@register.simple_tag
def load_content_block_js():
    """
    Renders the JavaScript elements required for a ``ContentBlockForm``
    """
    form = ContentBlockForm()

    return form.media["js"]
