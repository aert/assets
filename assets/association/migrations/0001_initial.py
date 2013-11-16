# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Student'
        db.create_table(u'association_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('adress', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('classroom', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('parent', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_registration', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now, null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'association', ['Student'])

        # Adding model 'Treasury'
        db.create_table(u'association_treasury', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'association', ['Treasury'])


    def backwards(self, orm):
        # Deleting model 'Student'
        db.delete_table(u'association_student')

        # Deleting model 'Treasury'
        db.delete_table(u'association_treasury')


    models = {
        u'association.student': {
            'Meta': {'object_name': 'Student'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'adress': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'classroom': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_registration': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'association.treasury': {
            'Meta': {'object_name': 'Treasury'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['association']