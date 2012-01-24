# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'InvoiceItem.amount'
        db.delete_column('invoices_invoiceitem', 'amount')

        # Adding field 'InvoiceItem.class_code'
        db.add_column('invoices_invoiceitem', 'class_code', self.gf('django.db.models.fields.CharField')(default='a', max_length=100), keep_default=False)

        # Adding field 'InvoiceItem.unit'
        db.add_column('invoices_invoiceitem', 'unit', self.gf('django.db.models.fields.CharField')(default='m', max_length=10), keep_default=False)

        # Adding field 'InvoiceItem.quantity'
        db.add_column('invoices_invoiceitem', 'quantity', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=8, decimal_places=2), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'InvoiceItem.amount'
        db.add_column('invoices_invoiceitem', 'amount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1), keep_default=False)

        # Deleting field 'InvoiceItem.class_code'
        db.delete_column('invoices_invoiceitem', 'class_code')

        # Deleting field 'InvoiceItem.unit'
        db.delete_column('invoices_invoiceitem', 'unit')

        # Deleting field 'InvoiceItem.quantity'
        db.delete_column('invoices_invoiceitem', 'quantity')


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
            'class_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoices.Invoice']"}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'net_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'product_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'tax': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['invoices']
