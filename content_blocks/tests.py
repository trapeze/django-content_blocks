from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import translation

from multilang.urlresolvers import reverse_for_language

from content_blocks.models import ContentBlockCore, ContentBlock, ImageBlockCore, ImageBlock


class ContentBlockTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test',
            is_superuser=True, is_staff=True
        )
        self.user.set_password('test')
        self.user.save()

        self.client.login(username='test', password='test')

    def testEditExistingBlock(self):
        core = ContentBlockCore.objects.create(name='test')

        for language, language_name in settings.LANGUAGES:
            block = ContentBlock.objects.create(core=core,
                language=language,
            )

            url = reverse_for_language('content_blocks_content_block_edit', lang=language,
                kwargs={'name':'test',}
            )
            response = self.client.get(url)

            expected = reverse_for_language(
                    'admin:content_blocks_contentblock_change',
                    lang=language,
                    args=(block.pk,))
            self.assertRedirects(response, expected, status_code=301)

    def testEditNonExistentBlock(self):
        for language, language_name in settings.LANGUAGES:
            translation.activate(language)
            name = u'test-%s' % language
            url = reverse_for_language('content_blocks_content_block_edit', lang=language,
                kwargs={'name':name,}
            )
            response = self.client.get(url)

            block = ContentBlock.objects.get(language=language, core__name=name)

            expected = reverse_for_language(
                    'admin:content_blocks_contentblock_change',
                    lang=language,
                    args=(block.pk,))
            self.assertRedirects(response, expected, status_code=301)
            translation.deactivate()


class ImageBlockTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test',
            is_superuser=True, is_staff=True
        )
        self.user.set_password('test')
        self.user.save()

        self.client.login(username='test', password='test')

    def testEditExistingBlock(self):
        core = ImageBlockCore.objects.create(name='test')

        for language, language_name in settings.LANGUAGES:
            block = ImageBlock.objects.create(core=core,
                language=language,
            )

            url = reverse_for_language('content_blocks_image_block_edit', lang=language,
                kwargs={'name':'test',}
            )
            response = self.client.get(url)

            expected = reverse_for_language(
                    'admin:content_blocks_imageblock_change',
                    lang=language,
                    args=(block.pk,))
            self.assertRedirects(response, expected, status_code=301)

    def testEditNonExistentBlock(self):
        for language, language_name in settings.LANGUAGES:
            translation.activate(language)
            name = u'test-%s' % language
            url = reverse_for_language('content_blocks_image_block_edit', lang=language,
                kwargs={'name':name,}
            )
            response = self.client.get(url)

            block = ImageBlock.objects.get(language=language, core__name=name)

            expected = reverse_for_language(
                    'admin:content_blocks_imageblock_change',
                    lang=language,
                    args=(block.pk,))
            self.assertRedirects(response, expected, status_code=301)
            translation.deactivate()
