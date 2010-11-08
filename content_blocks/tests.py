from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import translation


from content_blocks.models import ContentBlock, ImageBlock


class ContentBlockTestCase(TestCase):

    def setUp(self):
        translation.activate(settings.LANGUAGES[0][0])
        self.user = User.objects.create(username='test',
            is_superuser=True, is_staff=True
        )
        self.user.set_password('test')
        self.user.save()
        self.client.login(username='test', password='test')

    def testEditExistingBlock(self):
        block = ContentBlock.objects.create(name='test')

        url = reverse(
            'content_blocks_content_block_edit', kwargs={'name':'test'}
        )
        response = self.client.get(url)

        expected = reverse(
                'admin:content_blocks_contentblock_change',
                args=(block.pk,))
        self.assertRedirects(response, expected, status_code=301)

    def testEditNonExistentBlock(self):
        url = reverse(
            'content_blocks_content_block_edit', kwargs={'name': 'test-2'}
        )
        response = self.client.get(url)
        block = ContentBlock.objects.get(name='test-2')

        expected = reverse(
                'admin:content_blocks_contentblock_change',
                args=(block.pk,))
        self.assertRedirects(response, expected, status_code=301)


class ImageBlockTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test',
            is_superuser=True, is_staff=True
        )
        self.user.set_password('test')
        self.user.save()

        self.client.login(username='test', password='test')

    def testEditExistingBlock(self):
        block = ImageBlock.objects.create(name='test')

        url = reverse(
            'content_blocks_image_block_edit', kwargs={'name':'test'}
        )
        response = self.client.get(url)

        expected = reverse(
                'admin:content_blocks_imageblock_change',
                args=(block.pk,))
        self.assertRedirects(response, expected, status_code=301)

    def testEditNonExistentBlock(self):
        url = reverse(
            'content_blocks_image_block_edit', kwargs={'name':'test-2',}
        )
        response = self.client.get(url)

        block = ImageBlock.objects.get(name='test-2')

        expected = reverse(
                'admin:content_blocks_imageblock_change',
                args=(block.pk,))
        self.assertRedirects(response, expected, status_code=301)
