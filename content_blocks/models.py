from django.db import models
from django.utils.translation import ugettext_lazy as _

from linguo.manager import MultilingualManager
from linguo.models import MultilingualModel


class ContentBlock(MultilingualModel):
    """
    An editable content block.
    """
    name = models.SlugField(_("Name"), max_length=255, unique=True)
    content = models.TextField(_("Content"), blank=True)

    objects = MultilingualManager()

    class Meta:
        verbose_name = _("Content Block")
        verbose_name_plural = _("Content Blocks")
        translate = ('content',)

    def __unicode__(self):
        return self.name


class ImageBlock(MultilingualModel):
    """
    An editable Image Block.
    """
    name = models.SlugField(_("Name"), max_length=255, unique=True)
    image_file = models.FileField(upload_to='files/images', verbose_name=_('image file'))
    alternate_text = models.CharField(max_length=255, blank=True, verbose_name=_('alternate text'))
    link = models.CharField(max_length=255, blank=True, verbose_name=_('link'))

    objects = MultilingualManager()

    class Meta:
        verbose_name = _('Image Block')
        verbose_name_plural = _('Image Blocks')
        translate = ('image_file',)

    def __unicode__(self):
        return self.name
