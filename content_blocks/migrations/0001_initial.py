# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ContentBlock'
        db.create_table('content_blocks_contentblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_fr', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('content_blocks', ['ContentBlock'])

        # Adding model 'ImageBlock'
        db.create_table('content_blocks_imageblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('image_fr', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('alternate_text', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('content_blocks', ['ImageBlock'])


    def backwards(self, orm):
        
        # Deleting model 'ContentBlock'
        db.delete_table('content_blocks_contentblock')

        # Deleting model 'ImageBlock'
        db.delete_table('content_blocks_imageblock')


    models = {
        'content_blocks.contentblock': {
            'Meta': {'object_name': 'ContentBlock'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_fr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'content_blocks.imageblock': {
            'Meta': {'object_name': 'ImageBlock'},
            'alternate_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'image_fr': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['content_blocks']
