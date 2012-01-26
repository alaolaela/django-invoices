# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ProformaInvoice'
        db.create_table('invoices_proformainvoice', (
            ('invoice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['invoices.Invoice'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('invoices', ['ProformaInvoice'])


    def backwards(self, orm):
        
        # Deleting model 'ProformaInvoice'
        db.delete_table('invoices_proformainvoice')


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
            'sale_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'invoices.invoiceitem': {
            'Meta': {'object_name': 'InvoiceItem'},
            'class_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoices.Invoice']"}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'net_price': ('django.db.models.fields.FloatField', [], {}),
            'product_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'product_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'tax': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'invoices.proformainvoice': {
            'Meta': {'object_name': 'ProformaInvoice', '_ormbases': ['invoices.Invoice']},
            'invoice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoices.Invoice']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['invoices']
