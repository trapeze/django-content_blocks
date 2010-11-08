from django import template
from django.conf import settings

from content_blocks.models import ContentBlock, ImageBlock


register = template.Library()


@register.inclusion_tag("content_blocks/content_block.html", takes_context=True)
def show_content_block(context, name, editable=True, markup=True, amount='', method=None):
    """
    Renders the block with the given name and the context language
    If there block has no content and DEBUG is true, renders lorem ipsum text
    
        name     - The name of the block
        editable - Allow editing of the block
        markup   - Enable markup on the block
        amount   - A number (or variable) containing the number of paragraphs or words to generate (default is 1)
        method   - Either w for words, p for HTML paragraphs or b for plain-text paragraph blocks (default is b).
    
    amount
    
    Usage::

       {% show_content_block name [editable] [markup] [amount] [method] %}

    Example::

        {% show_content_block about True True 2 p %}
        
        Displays an editable content_block named 'about' with markup enabled.
        By default, it will contain two paragraphs of lorem text.
        
        {% show_content_block faq %}
        
        Display an editable content_block named 'faq'with markup enabled.  By
        default it will contain one paragraph of plain-text lorem.
        
    """
    try:
        block = ContentBlock.objects.get(name=name)
    except ContentBlock.DoesNotExist:
        block = None

    try:
        amount = int(amount)
    except ValueError:
        amount = None

    if method and not method in ('w', 'p', 'b'):
        raise template.TemplateSyntaxError("show_content_block -- method must be 'w', 'p', or 'b'")

    return {
        "name": name,
        "content_block": block,
        "wrapper": True,
        "editable": (editable is True or editable == "True"),
        "markup": (markup is True or markup == "True"),
        "perms": context.get("perms", None),
        "amount": amount,
        "method": method,
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE", None),
        "MEDIA_URL": context.get("MEDIA_URL", None),
        "DEBUG": settings.DEBUG,
    }


@register.inclusion_tag('content_blocks/_image_block.html', takes_context=True)
def show_image_block(context, name, editable=True, template='content_blocks/image_block.html'):
    try:
        block = ImageBlock.objects.get(name=name)
    except ImageBlock.DoesNotExist:
        block = None

    return {
        'name': name,
        'image_block': block,
        'editable': (editable is True or editable == 'True'),
        'template': template,
        'perms': context.get('perms', None),
        'LANGUAGE_CODE': context.get('LANGUAGE_CODE', None),
        'MEDIA_URL': context.get('MEDIA_URL', None),
        'DEBUG': settings.DEBUG,
    }
