from django.db import models
from django.utils.translation import ugettext_lazy as _

from linguo.manager import MultilingualManager
from linguo.models import MultilingualModel


class ContentBlock(MultilingualModel):
    """
    An editable content block.
    """
    name = models.SlugField(_("name"), max_length=255, unique=True)
    content = models.TextField(_("content"), blank=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    objects = MultilingualManager()

    class Meta:
        verbose_name = _("Content Block")
        verbose_name_plural = _("Content Blocks")
        translate = ('content',)

    def __unicode__(self):
        return self.name


class ImageBlock(MultilingualModel):
    """
    An editable image block.
    """
    name = models.SlugField(_("name"), max_length=255, unique=True)
    image = models.FileField(_('image file'), upload_to='files/images')
    alternate_text = models.CharField(_('alternate text'), max_length=255, blank=True)
    link = models.CharField(_('link'), max_length=255, blank=True)

    objects = MultilingualManager()

    class Meta:
        verbose_name = _('Image Block')
        verbose_name_plural = _('Image Blocks')
        translate = ('image',)

    def __unicode__(self):
        return self.name
