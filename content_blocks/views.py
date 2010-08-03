from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.views.generic import simple

from content_blocks.forms import ContentBlockForm, ImageBlockForm
from content_blocks.models import ContentBlockCore, ContentBlock, ImageBlockCore, ImageBlock
from content_blocks.utils import get_admin_edit_page


def _block_edit(request, model_name, name, model_class_core, model_class, form_class):
    block_core, __unused__ = model_class_core.objects.get_or_create(name=name)
    block, __unused__ = model_class.objects.get_or_create(
        core=block_core,
        language=request.LANGUAGE_CODE,
    )

    if request.is_ajax():
        if request.method == "POST":
            form = form_class(request.POST, instance=block)

            if form.is_valid():
                block = form.save()

                return simple.direct_to_template(request, "content_blocks/%s.html" % model_name, extra_context={
                    "%s" % model_name: block,
                    "content_mode": True,
                    "editable": True,
                    "markup": True,
                    "DEBUG": settings.DEBUG,
                })
        elif request.GET.has_key("cancel"):
            return simple.direct_to_template(request, "content_blocks/%s.html" % model_name, extra_context={
                "%s" % model_name: block,
                "just_content": True,
                "editable": True,
                "markup": True,
                "DEBUG": settings.DEBUG,
            })
        else:
            form = form_class(instance=block)

        return simple.direct_to_template(request, "content_blocks/%s_edit.html" % model_name, extra_context={
            "form": form,
            "%s" % model_name: block,
        })
    else:
        return simple.redirect_to(request, get_admin_edit_page(block))


@permission_required("content_blocks.contentblock")
def content_block_edit(request, name):
    """
    Edit view for a ContentBlock object, creates the block if it doesn't exist
    """
    return _block_edit(
        request, 'content_block', name,
        ContentBlockCore, ContentBlock, ContentBlockForm)


@permission_required("content_blocks.imageblock")
def image_block_edit(request, name):
    """
    Edit view for a ImageBlock object, creates the block if it doesn't exist
    """
    return _block_edit(
        request, 'image_block', name,
        ImageBlockCore, ImageBlock, ImageBlockForm)
