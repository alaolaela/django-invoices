# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Invoice.status'
        db.add_column('invoices_invoice', 'status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Invoice.status'
        db.delete_column('invoices_invoice', 'status')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'invoices.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'currency': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'customer_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'customer_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {}),
            'date_payment': ('django.db.models.fields.DateField', [], {}),
            'date_sale': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'payment_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sale_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'invoices.invoiceitem': {
            'Meta': {'object_name': 'InvoiceItem'},
            'amount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoices.Invoice']"}),
            'net_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'product_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tax': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['invoices']
