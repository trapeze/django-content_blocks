from django import template
from django.conf import settings

from content_blocks.forms import ContentBlockForm
from content_blocks.models import ContentBlock


register = template.Library()


@register.inclusion_tag("content_blocks/block.html", takes_context=True)
def show_content_block(context, name, editable=True, markup=True, amount=''):
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

    try:
        amount = int(amount)
    except ValueError:
        amount = None

    return {
        "name": name,
        "block": block,
        "editable": (editable is True or editable == "True"),
        "markup": (markup is True or markup == "True"),
        "perms": context.get("perms", None),
        "amount": amount,
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE", None),
        "MEDIA_URL": context.get("MEDIA_URL", None),
        "DEBUG": settings.DEBUG,
    }
