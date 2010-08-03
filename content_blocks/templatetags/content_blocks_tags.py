from django import template
from django.conf import settings

from content_blocks.models import ContentBlock, ImageBlock


register = template.Library()


@register.inclusion_tag("content_blocks/content_block.html", takes_context=True)
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
        "content_block": block,
        "editable": (editable is True or editable == "True"),
        "markup": (markup is True or markup == "True"),
        "perms": context.get("perms", None),
        "amount": amount,
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE", None),
        "MEDIA_URL": context.get("MEDIA_URL", None),
        "DEBUG": settings.DEBUG,
    }


@register.tag
def show_content_block_as_text(parser, token):
    try:
        tag_name, block_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument." % token.contents.split_contents()[0]
    return ShowContentBlockAsTextNode(block_name)


class ShowContentBlockAsTextNode(template.Node):
    def __init__(self, block_name):
        self.block_name = template.Variable(block_name)

    def render(self, context):
        try:
            block = ContentBlock.objects.get(
                core__name=self.block_name.resolve(context),
                language=context.get("LANGUAGE_CODE", None)
            )
        except ContentBlock.DoesNotExist:
            return ''
        return block.content


@register.inclusion_tag('content_blocks/_image_block.html', takes_context=True)
def show_image_block(context, name, editable=True, template='content_blocks/image_block.html'):
    try:
        block = ImageBlock.objects.get(
            core__name=name,
            language=context.get('LANGUAGE_CODE', None)
        )
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
