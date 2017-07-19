# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'tasks_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('time', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('serviceman', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dpartment', self.gf('django.db.models.fields.CharField')(default='tech', max_length=64)),
            ('responsibleman', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dpartment1', self.gf('django.db.models.fields.CharField')(default='tech', max_length=64)),
            ('task', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('taskman', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tasktime', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('issue_des', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('issue_solve', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('feedback', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('leaderview', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('review', self.gf('django.db.models.fields.CharField')(default='\xe6\x9c\xaa\xe5\xae\xa1\xe6\xa0\xb8', max_length=50)),
        ))
        db.send_create_signal(u'tasks', ['Task'])

        # Adding model 'Branch'
        db.create_table(u'tasks_branch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('time', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('serviceman', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dpartment', self.gf('django.db.models.fields.CharField')(default='tech', max_length=64)),
            ('operation', self.gf('django.db.models.fields.CharField')(default='branch', max_length=64)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('operaman', self.gf('django.db.models.fields.CharField')(default='zjc', max_length=64)),
            ('developman', self.gf('django.db.models.fields.CharField')(default='lilili', max_length=64)),
            ('branch_des', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('review', self.gf('django.db.models.fields.CharField')(default='\xe6\x9c\xaa\xe5\xae\xa1\xe6\xa0\xb8', max_length=50)),
            ('solve', self.gf('django.db.models.fields.CharField')(default='\xe6\x9c\xaa\xe6\x89\xa7\xe8\xa1\x8c', max_length=50)),
        ))
        db.send_create_signal(u'tasks', ['Branch'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table(u'tasks_task')

        # Deleting model 'Branch'
        db.delete_table(u'tasks_branch')


    models = {
        u'tasks.branch': {
            'Meta': {'object_name': 'Branch'},
            'branch_des': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'developman': ('django.db.models.fields.CharField', [], {'default': "'lilili'", 'max_length': '64'}),
            'dpartment': ('django.db.models.fields.CharField', [], {'default': "'tech'", 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operaman': ('django.db.models.fields.CharField', [], {'default': "'zjc'", 'max_length': '64'}),
            'operation': ('django.db.models.fields.CharField', [], {'default': "'branch'", 'max_length': '64'}),
            'review': ('django.db.models.fields.CharField', [], {'default': "'\\xe6\\x9c\\xaa\\xe5\\xae\\xa1\\xe6\\xa0\\xb8'", 'max_length': '50'}),
            'serviceman': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'solve': ('django.db.models.fields.CharField', [], {'default': "'\\xe6\\x9c\\xaa\\xe6\\x89\\xa7\\xe8\\xa1\\x8c'", 'max_length': '50'}),
            'time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'dpartment': ('django.db.models.fields.CharField', [], {'default': "'tech'", 'max_length': '64'}),
            'dpartment1': ('django.db.models.fields.CharField', [], {'default': "'tech'", 'max_length': '64'}),
            'feedback': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_des': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'issue_solve': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'leaderview': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'responsibleman': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'review': ('django.db.models.fields.CharField', [], {'default': "'\\xe6\\x9c\\xaa\\xe5\\xae\\xa1\\xe6\\xa0\\xb8'", 'max_length': '50'}),
            'serviceman': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'taskman': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tasktime': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tasks']