from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.core import serializers
from django.views.generic import simple

from content_blocks.forms import ContentBlockForm, ImageBlockForm
from content_blocks.models import ContentBlock, ImageBlock
from content_blocks.utils import get_admin_list_page, get_admin_edit_page


def _block_edit(request, model_name, name, model_class, form_class):
    block, __unused__ = model_class.objects.get_or_create(name=name)

    markup = request.GET.get("markup", "True") == "True"
    if request.is_ajax():
        if request.method == "POST":
            form = form_class(request.POST, instance=block)

            if form.is_valid():
                block = form.save()

                return simple.direct_to_template(request, "content_blocks/%s.html" % model_name, extra_context={
                    "%s" % model_name: block,
                    "wrapper": False,
                    "editable": True,
                    "markup": markup,
                    "DEBUG": settings.DEBUG,
                })
        elif request.GET.has_key("cancel"):
            return simple.direct_to_template(request, "content_blocks/%s.html" % model_name, extra_context={
                "%s" % model_name: block,
                "wrapper": False,
                "editable": True,
                "markup": markup,
                "DEBUG": settings.DEBUG,
            })
        else:
            form = form_class(instance=block)

        return simple.direct_to_template(request, "content_blocks/%s_edit.html" % model_name, extra_context={
            "form": form,
            "%s" % model_name: block,
            "markup": markup,
        })
    else:
        return simple.redirect_to(request, get_admin_edit_page(block))


@permission_required("content_blocks.change_contentblock")
def content_block_edit(request, name):
    """
    Edit view for a ContentBlock object, creates the block if it doesn't exist
    """
    return _block_edit(
        request, 'content_block', name, ContentBlock, ContentBlockForm
    )


@permission_required("content_blocks.change_imageblock")
def image_block_edit(request, name):
    """
    Edit view for a ImageBlock object, creates the block if it doesn't exist
    """
    return _block_edit(
        request, 'image_block', name, ImageBlock, ImageBlockForm
    )

@permission_required("content_blocks.change_contentblock")
def content_block_json_upload(request):
    """
    Upload a group of ContentBlocks in JSON format
    """
    if 'json_data' in request.FILES:
        try:
            for new_block in serializers.deserialize('json', request.FILES['json_data'].read()):
                existing_query = ContentBlock.objects.filter(name=new_block.object.name)
                if existing_query:
                    existing_block = existing_query.get()
                    new_block.object.id = existing_block.id
                    new_block.save()
                    continue

                else:
                    new_block.object.id = None
                    new_block.save()

            messages.success(request, 'JSON Content Blocks Successfully imported.')
        except ValueError:
            messages.error(request, 'JSON File Invalid')
    
    return simple.redirect_to(request, get_admin_list_page(ContentBlock))
