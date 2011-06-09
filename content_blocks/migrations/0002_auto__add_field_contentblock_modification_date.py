# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ContentBlock.modification_date'
        db.add_column('content_blocks_contentblock', 'modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2011, 6, 9, 10, 6, 19, 801297), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ContentBlock.modification_date'
        db.delete_column('content_blocks_contentblock', 'modification_date')


    models = {
        'content_blocks.contentblock': {
            'Meta': {'object_name': 'ContentBlock'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_fr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
