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
