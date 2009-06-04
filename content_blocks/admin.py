from django.contrib import admin

from multilang.admin import LangTranslatableModelAdmin, LangAgnosticModelAdmin

from content_blocks.models import ContentBlockCore, ContentBlock


class ContentBlockAdmin(LangTranslatableModelAdmin):
    list_display = ('core', 'language', )
    list_filter = ('language', )


class ContentBlockCoreAdmin(LangAgnosticModelAdmin):
    list_display = ('name', )


admin.site.register(ContentBlock, ContentBlockAdmin)
admin.site.register(ContentBlockCore, ContentBlockCoreAdmin)
