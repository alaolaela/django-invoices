# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Invoice'
        db.create_table('invoices_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('date_created', self.gf('django.db.models.fields.DateField')()),
            ('date_sale', self.gf('django.db.models.fields.DateField')()),
            ('date_payment', self.gf('django.db.models.fields.DateField')()),
            ('currency', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('payment_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sale_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('customer_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('customer_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('invoices', ['Invoice'])

        # Adding model 'InvoiceItem'
        db.create_table('invoices_invoiceitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoices.Invoice'])),
            ('product_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('product_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('net_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('tax', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('amount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal('invoices', ['InvoiceItem'])


    def backwards(self, orm):
        
        # Deleting model 'Invoice'
        db.delete_table('invoices_invoice')

        # Deleting model 'InvoiceItem'
        db.delete_table('invoices_invoiceitem')


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
            'sale_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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
