# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Book'
        db.create_table('amazon_book', (
            ('published_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=300)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('amazon_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('medium_image_url', self.gf('django.db.models.fields.URLField')(max_length=300, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('small_image_url', self.gf('django.db.models.fields.URLField')(max_length=300, null=True, blank=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None, db_index=True)),
            ('large_image_url', self.gf('django.db.models.fields.URLField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('amazon', ['Book'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Book'
        db.delete_table('amazon_book')
    
    
    models = {
        'amazon.book': {
            'Meta': {'object_name': 'Book'},
            'amazon_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'large_image_url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'medium_image_url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'published_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'small_image_url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '300'})
        }
    }
    
    complete_apps = ['amazon']
