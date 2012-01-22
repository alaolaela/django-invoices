# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Invoice'
        db.create_table('documents_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('customer_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('documents', ['Invoice'])

        # Adding model 'Document'
        db.create_table('documents_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codename', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('footer', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('margin_top', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=15)),
            ('margin_bottom', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=30)),
            ('margin_left', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=15)),
            ('margin_right', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=15)),
        ))
        db.send_create_signal('documents', ['Document'])


    def backwards(self, orm):
        
        # Deleting model 'Invoice'
        db.delete_table('documents_invoice')

        # Deleting model 'Document'
        db.delete_table('documents_document')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'documents.document': {
            'Meta': {'object_name': 'Document'},
            'codename': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'footer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'margin_bottom': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'margin_left': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '15'}),
            'margin_right': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '15'}),
            'margin_top': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '15'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'documents.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'customer_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'customer_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['documents']
