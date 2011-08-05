import datetime

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import translation


from content_blocks.models import ContentBlock, ImageBlock


class ContentBlockTestCase(TestCase):

    def setUp(self):
        translation.activate(settings.LANGUAGES[0][0])
        self.user = User.objects.create(username='test', is_staff=True)
        perm = Permission.objects.get(codename="change_contentblock")
        self.user.user_permissions.add(perm)
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
        before = datetime.datetime.now()
        block = ContentBlock.objects.create(name='test')
        block.name='test1'
        block.save()
        after = datetime.datetime.now()
        self.assertTrue(block.modification_date > before and block.modification_date < after)

    def test_import_content_blocks_from_json_adds_new_content_blocks_to_the_db(self):
        post_data = {
            'json_data': open('../lib/content_blocks/tests/files/test_data1.json'),
        }
        
        url = reverse(
            'content_blocks_json_upload',
        )
        response = self.client.post(
            url,
            post_data,
            follow=True,
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(ContentBlock.objects.all().count(), 2)
        self.assertEquals(ContentBlock.objects.get(name='block_name').content, 'Some text!')
        self.assertEquals(ContentBlock.objects.get(name='another_block').content, 'Some More Text!')

    def test_import_content_blocks_from_json_with_existing_slugs_updates_content_blocks_in_the_db(self):
        block1 = ContentBlock.objects.create(name='block1', content='content1')
        block2 = ContentBlock.objects.create(name='block2', content='content2')
        
        post_data = {
            'json_data': open('../lib/content_blocks/tests/files/test_data2.json'),
        }
        
        url = reverse(
            'content_blocks_json_upload',
        )
        response = self.client.post(
            url,
            post_data,
            follow=True,
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(ContentBlock.objects.all().count(), 2)
        self.assertEquals(ContentBlock.objects.get(name='block1').content, 'newcontent1')
        self.assertEquals(ContentBlock.objects.get(name='block2').content, 'newcontent2')

    def test_import_content_blocks_with_existing_id_but_different_slug_does_not_overwrite_existing_content_block(self):
        block1 = ContentBlock.objects.create(name='block1', content='content1')
        block2 = ContentBlock.objects.create(name='block2', content='content2')
        
        post_data = {
            'json_data': open('../lib/content_blocks/tests/files/test_data3.json'),
        }
        
        url = reverse(
            'content_blocks_json_upload',
        )
        response = self.client.post(
            url,
            post_data,
            follow=True,
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(ContentBlock.objects.all().count(), 3)
        self.assertEquals(ContentBlock.objects.get(name='block1').content, 'content1')
        self.assertEquals(ContentBlock.objects.get(name='block2').content, 'newcontent2')
        self.assertEquals(ContentBlock.objects.get(name='block3').content, 'newcontent3')
    
    def test_invalid_json_file_redirects_and_displays_error(self):
        block1 = ContentBlock.objects.create(name='block1', content='content1')
        block2 = ContentBlock.objects.create(name='block2', content='content2')
        
        post_data = {
            'json_data': open('../lib/content_blocks/tests/files/invalid_data.json'),
        }
        
        url = reverse(
            'content_blocks_json_upload',
        )
        response = self.client.post(
            url,
            post_data,
            follow=True,
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(ContentBlock.objects.all().count(), 2)
        self.assertEquals(ContentBlock.objects.get(name='block1').content, 'content1')
        self.assertEquals(ContentBlock.objects.get(name='block2').content, 'content2')


class ImageBlockTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', is_staff=True)
        perm = Permission.objects.get(codename="change_imageblock")
        self.user.user_permissions.add(perm)
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
