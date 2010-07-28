from django.db import models
from django.utils.translation import ugettext_lazy as _

from multilang.models import LangAgnostic, LangTranslatable


class ContentBlockCore(LangAgnostic):
    """
    Non-translatable fields for the ContentBlock model
    """
    name = models.SlugField(_("Name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Content Block")
        verbose_name_plural = _("Content Blocks")

    def __unicode__(self):
        return self.name


class ContentBlock(LangTranslatable):
    """
    Translatable fields for the ContentBlock model
    """
    core = models.ForeignKey(
        ContentBlockCore, verbose_name=_("Core"), related_name="translations"
    )
    content = models.TextField(_("Content"), blank=True)

    class Meta:
        verbose_name = _("Content Block Translation")
        verbose_name_plural = _("Content Block Translations")

    def __unicode__(self):
        return '%s - %s' % (self.name, self.language)

    @property
    def name(self):
        return self.core.name


class ImageBlockCore(LangAgnostic):
    """
    Non-translatable fields for the ContentBlock model
    """
    name = models.SlugField(_("Name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _('Image Block')
        verbose_name_plural = _('Image Blocks')
        

    def __unicode__(self):
        return self.name


class ImageBlock(LangTranslatable):
    """
    Translatable fields for the ContentBlock model
    """
    core = models.ForeignKey(
        ImageBlockCore, verbose_name=_('core'), related_name='translations'
    )
    image_file = models.FileField(upload_to='files/images', verbose_name=_('image file'))
    alternate_text = models.CharField(max_length=255, blank=True, verbose_name=_('alternate text'))
    link = models.CharField(max_length=255, blank=True, verbose_name=_('link'))

    class Meta:
        verbose_name = _('Image Block Translation')
        verbose_name_plural = _('Image Block Translations')

    def __unicode__(self):
        return '%s - %s' % (self.name, self.language)

    @property
    def name(self):
        return self.core.name
