from django.contrib import admin

from content_blocks.models import ContentBlock, ImageBlock


class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('name','modification_date',)

admin.site.register(ContentBlock, ContentBlockAdmin)

admin.site.register(ImageBlock)
