# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table('sopin_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True)),
            ('unit_symbol', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('unit_weight', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, default=1, max_digits=6)),
            ('purchase_threshold', self.gf('django.db.models.fields.IntegerField')(default=21)),
            ('extended_threshold', self.gf('django.db.models.fields.IntegerField')(blank=True, default=0)),
            ('heavy', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('data', ['Item'])

        # Adding model 'Purchase'
        db.create_table('sopin_purchase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Item'])),
            ('date', self.gf('django.db.models.fields.DateField')(db_index=True, default=datetime.datetime(2014, 5, 31, 0, 0))),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, default=1, max_digits=6)),
        ))
        db.send_create_signal('data', ['Purchase'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table('sopin_item')

        # Deleting model 'Purchase'
        db.delete_table('sopin_purchase')


    models = {
        'data.item': {
            'Meta': {'object_name': 'Item', 'db_table': "'sopin_item'", 'ordering': "['name']"},
            'extended_threshold': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'heavy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'purchase_threshold': ('django.db.models.fields.IntegerField', [], {'default': '21'}),
            'unit_symbol': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'unit_weight': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '1', 'max_digits': '6'})
        },
        'data.purchase': {
            'Meta': {'object_name': 'Purchase', 'db_table': "'sopin_purchase'", 'ordering': "['-date']"},
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'default': 'datetime.datetime(2014, 5, 31, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Item']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '1', 'max_digits': '6'})
        }
    }

    complete_apps = ['data']