# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Customer'
        db.create_table('customers_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_index=True)),
            ('kind', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('broker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brokers.Broker'], null=True, blank=True)),
            ('representative', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('tel_nr', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=90, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=90, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('provision', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('customers', ['Customer'])

        # Adding model 'Offer'
        db.create_table('customers_offer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('offer_type', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('priority', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customers.Customer'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('requirements', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('customers', ['Offer'])


    def backwards(self, orm):
        
        # Deleting model 'Customer'
        db.delete_table('customers_customer')

        # Deleting model 'Offer'
        db.delete_table('customers_offer')


    models = {
        'brokers.broker': {
            'Meta': {'object_name': 'Broker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '90', 'null': 'True', 'blank': 'True'}),
            'broker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brokers.Broker']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '90', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'provision': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'representative': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'tel_nr': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'customers.offer': {
            'Meta': {'object_name': 'Offer'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'priority': ('django.db.models.fields.SmallIntegerField', [], {}),
            'requirements': ('django.db.models.fields.TextField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['customers']
