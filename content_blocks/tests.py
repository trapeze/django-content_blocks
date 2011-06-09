import datetime

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

    def test_edit_existing_block_redirects(self):
        block = ContentBlock.objects.create(name='test')
        url = reverse(
            'content_blocks_content_block_edit', kwargs={'name': 'test'}
        )
        response = self.client.get(url)
        expected = reverse(
            'admin:content_blocks_contentblock_change', args=(block.pk,)
        )
        self.assertRedirects(response, expected, status_code=301)

    def test_edit_non_existent_block_redirects(self):
        url = reverse(
            'content_blocks_content_block_edit', kwargs={'name': 'test-new'}
        )
        response = self.client.get(url)
        block = ContentBlock.objects.get(name='test-new')
        expected = reverse(
            'admin:content_blocks_contentblock_change', args=(block.pk,)
        )
        self.assertRedirects(response, expected, status_code=301)
        
    def test_create_new_content_block_object_sets_modification_date(self):
        before = datetime.datetime.now()
        block = ContentBlock.objects.create(name='test')
        after = datetime.datetime.now()
        self.assertTrue(block.modification_date > before and block.modification_date < after)
        
    def test_update_content_block_object_sets_modification_date(self):
        now = datetime.datetime.now()
        block = ContentBlock.objects.create(name='test')
        block.name='test1'
        block.save()
        after = datetime.datetime.now()
        self.assertTrue(block.modification_date > before and block.modification_date < after)
        

class ImageBlockTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test',
            is_superuser=True, is_staff=True
        )
        self.user.set_password('test')
        self.user.save()
        self.client.login(username='test', password='test')

    def test_edit_existing_block_redirect(self):
        block = ImageBlock.objects.create(name='test')
        url = reverse(
            'content_blocks_image_block_edit', kwargs={'name': 'test'}
        )
        response = self.client.get(url)
        expected = reverse(
            'admin:content_blocks_imageblock_change', args=(block.pk,)
        )
        self.assertRedirects(response, expected, status_code=301)

    def test_edit_non_existent_block_redirects(self):
        url = reverse(
            'content_blocks_image_block_edit', kwargs={'name':'test-2',}
        )
        response = self.client.get(url)
        block = ImageBlock.objects.get(name='test-2')
        expected = reverse(
            'admin:content_blocks_imageblock_change', args=(block.pk,)
        )
        self.assertRedirects(response, expected, status_code=301)
