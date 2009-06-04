from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.views.generic import simple

from content_blocks.forms import ContentBlockForm
from content_blocks.models import ContentBlockCore, ContentBlock


@permission_required("content_blocks.contentblock")
def edit(request, name):
    """
    Edit view for a ContentBlock object, creates the block if it doesn't exist
    """
    block_core, __unused__ = ContentBlockCore.objects.get_or_create(name=name)
    block, __unused__ = ContentBlock.objects.get_or_create(
        core=block_core,
        language=request.LANGUAGE_CODE,
    )

    if request.is_ajax():
        if request.method == "POST":
            form = ContentBlockForm(request.POST, instance=block)

            if form.is_valid():
                block = form.save()

                return simple.direct_to_template(request, "content_blocks/block.html", extra_context={
                    "block": block,
                    "editable": True,
                    "markup": True,
                    "DEBUG": settings.DEBUG,
                })
        elif request.GET.has_key("cancel"):
            return simple.direct_to_template(request, "content_blocks/block.html", extra_context={
                "block": block,
                "editable": True,
                "markup": True,
                "DEBUG": settings.DEBUG,
            })
        else:
            form = ContentBlockForm(instance=block)

        return simple.direct_to_template(request, "content_blocks/edit.html", extra_context={
            "form": form,
            "block": block,
        })
    else:
        return simple.redirect_to(
            request, "/%(lang)s/admin/content_blocks/contentblock/%(id)d/" % {
                "lang": request.LANGUAGE_CODE,
                "id": block.pk,
            }
        )
