Content Blocks
==============

This application provides a model and the necessary template tags for defining
editable content block areas in the templates. Without any need for initial
data, it can generate the blocks in the database when required. It also
provides an "Edit" link next to the blocks. If JavaScript is enabled and the
included JS class is loaded, these links enable AJAX-based, inline editing
of content right in the page. Otherwise, they become simple links to the admin
area of the selected block.


Installation
------------

To install Content Blocks, include it in your ``INSTALLED_APPS`` list, under
your project's settings.py file. Install `markdown.py` as well.

Multilingual support is powered by Linguo Django application.

To render the content using markdown and show placeholder text when DEBUG is set
to True, the app depends on ``markup`` and ``webdesign`` applications,
included in ``django.contrib``.

    INSTALLED_APPS = (
        'django.contrib.markup',
        'django.contrib.webdesign',

        'linguo',
        'content_blocks',
    )

The second step is to include content_blocks.urls in your urls.py:

    urlpatterns = patterns('',
        url(_(r'^content-blocks/'), include('content_blocks.urls')),
    )

Finally, you'll need to force admin into English mode or content blocks
will not work properly when editing in other languages. (See ticket #001011-630 for more details). Append the following to `MIDDLEWARE_CLASSES` in settings.py:

    MIDDLEWARE_CLASSES = (
        # ...
        'content_blocks.middleware.ForceEnglishInAdminMiddleware',
    )

After running ./manage.py syncdb, app will be ready to use.


Upgrade Instructions
--------------------

To upgrade Content Blocks from a pre-2.X version to 2.X you will need to follow these instructions.

First you will need to export your existing data into a format which can be read by the new content blocks using the following script, which you should
copy and paste into a Django console started with ./manage.py shell:

---------------------------------------------------------------------------
import json

from content_blocks.models import ContentBlockCore, ImageBlockCore

def export_content_blocks():
    blocks = []
    for block in ContentBlockCore.objects.all():
        block_en = block.translations.filter(language='en').get()
        block_fr = block.translations.filter(language='fr')
        if block_fr:
            block_fr = block_fr.get()
        else:
            block_fr = None
        block_json = {
            'pk'      : block.id,
            'model'   : 'content_blocks.contentblock',
            'fields'  : {
                'name'        : block.name,
                'content'     : block_en.content,
                'content_fr'  : block_fr.content if block_fr else block_en.content,
            },
        }
        blocks.append(block_json)
    for block in ImageBlockCore.objects.all():
        image_en = block.translations.filter(language='en').get()
        image_fr = block.translations.filter(language='fr')
        if image_fr:
            image_fr = image_fr.get()
        else:
            image_fr = None
        block_json = {
            'pk'      : block.id,
            'model'   : 'content_blocks.imageblock',
            'fields'  : {
                'name'                : block.name,
                'link'                : image_en.link,
                'link_fr'             : image_fr.link if image_fr else image_en.link,
                'alternate_text'      : image_en.alternate_text,
                'alternate_text_fr'   : image_fr.alternate_text if image_fr else image_en.alternate_text,
                'image'               : ('files' + image_en.image_file.path.split('files')[1]) if image_en.image_file.name else '',
                'image_fr'            : ('files' + image_fr.image_file.path.split('files')[1]) if image_fr and image_fr.image_file.name else '',
            },
        } 
        blocks.append(block_json) 
    outfile = open('content_blocks.json', 'w')
    outfile.write(json.dumps(blocks))
    outfile.close() 
    print 'Done'

export_content_blocks()
---------------------------------------------------------------------------

When that is complete it will print 'Done' and you can exit the shell.  
Now you will find a file called 'content_blocks.json' in your project root, which contains the JSON
formatted data for the projects Content and Image blocks.

Add the latest version of Content Blocks to your project.

Now you will need to remove the old tables from the database.  
If this is not a local deployment, make sure you perform a full backup before performing this step.

    psql -U <projectname>team <projectname>_<site> 

    drop table content_blocks_contentblock;
    drop table content_blocks_contentblockcore;
    drop table content_blocks_imageblock;
    drop table content_blocks_imageblockcore;

With the old tables gone, you can now create the new tables using

    ./manage.py syncdb

And answer yes when it asks if you want to remove the unused tables

Finally we load our old data back into the database with

    ./manage.py loaddata content_blocks.json

Which should report that it loaded a number of objects from 1 fixture.

Now ensure that the data was correctly loaded by going into the Admin 
and looking at both the Content Blocks and Image Blocks sections.



Template Tags
-------------

Content Blocks can only be used through template tags. To define a block,
simply load the tag library and call it as such:

    {% load content_blocks_tags %}
    {% show_content_block "about" %}
    {% show_image_block "ceo" %}

``show_content_block`` only requires the unique identifier name of the block by
default. You can also provide three optional parameters: ``editable``,
``markup``, and ``amount``. If ``editable`` is set to "False", the edit link is
omitted. Similarly, if ``markup`` is set to "False", markdown is not applied to
the content. If ``amount`` is set to a number (or variable representing a
number) and there is no content for the block in the database, you will get
that many words of "lorem" text (if omitted or set to an empty string, you will
get the standard paragraph of approximately 70 words).

    {% show_content_block "about" "False" "False" 7 %}

To enable JavaScript functionality, you should import the JS enhancement app for
content blocks.

``show_image_block`` optionally takes a template name to override the
the template used to render the image block on a per image block basis:

    {% show_image_block "ceo" True "ceo_image_block.html" %}
