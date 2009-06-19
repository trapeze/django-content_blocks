from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import translation

from multilang.urlresolvers import reverse_for_language
from content_blocks.models import ContentBlockCore, ContentBlock


class ContentBlocksTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test',
            is_superuser=True, is_staff=True
        )
        self.user.set_password('test')
        self.user.save()

        self.client.login(username='test', password='test')

    def testEditExistingBlock(self):
        core = ContentBlockCore.objects.create(name='test')

        for lang in settings.LANGUAGES:
            block = ContentBlock.objects.create(core=core,
                language=lang[0],
            )

            url = reverse_for_language('content_blocks_edit', lang=lang[0],
                kwargs={'name':'test',}
            )
            response = self.client.get(url)

            admin_base_url = reverse_for_language(admin.site.root, lang=lang[0],
                args=('',)
            )
            expected = u'%scontent_blocks/contentblock/%d/' % (admin_base_url,
                block.pk
            )
            self.assertRedirects(response, expected, status_code=301)

    def testEditNonExistentBlock(self):
        for lang in settings.LANGUAGES:
            translation.activate(lang[0])
            name = u'test-%s' % lang[0]
            url = reverse_for_language('content_blocks_edit', lang=lang[0],
                kwargs={'name':name,}
            )
            response = self.client.get(url)

            block = ContentBlock.objects.get(language=lang[0], core__name=name)

            admin_base_url = reverse_for_language(admin.site.root, lang=lang[0],
                args=('',)
            )
            expected = u'%scontent_blocks/contentblock/%d/' % (admin_base_url,
                block.pk
            )
            self.assertRedirects(response, expected, status_code=301)
            translation.deactivate()
