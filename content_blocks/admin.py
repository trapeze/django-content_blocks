import datetime

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponse

from content_blocks.models import ContentBlock, ImageBlock


class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('name','modification_date',)
    actions = ['export_selected_objects']
    
    def export_selected_objects(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        response = HttpResponse(mimetype="application/json")
        response['Content-Disposition'] = u'attachment; filename=content_blocks-%s.json' % \
        (datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        
        serializers.serialize("json", queryset, stream=response)
    
        return response
    export_selected_objects.short_description = "Export to JSON"
    
admin.site.register(ContentBlock, ContentBlockAdmin)

admin.site.register(ImageBlock)
