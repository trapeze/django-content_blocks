from django.conf.urls.defaults import *


urlpatterns = patterns('content_blocks.views',
    url(r'^content-block-edit/(?P<name>[\w-]+)/$', 'content_block_edit', name='content_blocks_content_block_edit'),
    url(r'^image-block-edit/(?P<name>[\w-]+)/$', 'image_block_edit', name='content_blocks_image_block_edit'),
)
