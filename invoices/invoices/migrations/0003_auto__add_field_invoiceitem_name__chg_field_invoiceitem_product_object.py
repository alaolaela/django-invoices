# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'InvoiceItem.name'
        db.add_column('invoices_invoiceitem', 'name', self.gf('django.db.models.fields.TextField')(default=0), keep_default=False)

        # Changing field 'InvoiceItem.product_object_id'
        db.alter_column('invoices_invoiceitem', 'product_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'InvoiceItem.product_content_type'
        db.alter_column('invoices_invoiceitem', 'product_content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True))


    def backwards(self, orm):
        
        # Deleting field 'InvoiceItem.name'
        db.delete_column('invoices_invoiceitem', 'name')

        # User chose to not deal with backwards NULL issues for 'InvoiceItem.product_object_id'
        raise RuntimeError("Cannot reverse this migration. 'InvoiceItem.product_object_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'InvoiceItem.product_content_type'
        raise RuntimeError("Cannot reverse this migration. 'InvoiceItem.product_content_type' and its values cannot be restored.")


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
            'currency': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'customer_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'customer_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {}),
            'date_payment': ('django.db.models.fields.DateField', [], {}),
            'date_sale': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'payment_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'sale_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'invoices.invoiceitem': {
            'Meta': {'object_name': 'InvoiceItem'},
            'amount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoices.Invoice']"}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'net_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'product_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'tax': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['invoices']
