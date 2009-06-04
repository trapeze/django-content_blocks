from django.conf.urls.defaults import *


urlpatterns = patterns('content_blocks.views',
    url(r'^edit/(?P<name>[\w-]+)/$', 'edit', name='content_blocks_edit'),
)
