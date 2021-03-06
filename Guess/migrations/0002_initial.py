# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'Guess_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('point', self.gf('django.db.models.fields.IntegerField')(default=1000)),
            ('expertise', self.gf('django.db.models.fields.TextField')(default='N/A')),
            ('win', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lose', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('game', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('point_per_game', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'Guess', ['Person'])

        # Adding model 'Game'
        db.create_table(u'Guess_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('headline', self.gf('django.db.models.fields.TextField')()),
            ('begin', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expire', self.gf('django.db.models.fields.DateTimeField')()),
            ('name_home', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('price_home', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('num_home', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name_away', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('price_away', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('num_away', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('outcome', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ended', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Guess', ['Game'])

        # Adding model 'Betting'
        db.create_table(u'Guess_betting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('better', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Guess.Person'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Guess.Game'])),
            ('side', self.gf('django.db.models.fields.BooleanField')()),
            ('num', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('outcome', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('price_at_buy', self.gf('django.db.models.fields.FloatField')()),
            ('price_at_sell', self.gf('django.db.models.fields.FloatField')()),
            ('cleared', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Guess', ['Betting'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'Guess_person')

        # Deleting model 'Game'
        db.delete_table(u'Guess_game')

        # Deleting model 'Betting'
        db.delete_table(u'Guess_betting')


    models = {
        u'Guess.betting': {
            'Meta': {'object_name': 'Betting'},
            'better': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Guess.Person']"}),
            'cleared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Guess.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'outcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_at_buy': ('django.db.models.fields.FloatField', [], {}),
            'price_at_sell': ('django.db.models.fields.FloatField', [], {}),
            'side': ('django.db.models.fields.BooleanField', [], {})
        },
        u'Guess.game': {
            'Meta': {'ordering': "('expire',)", 'object_name': 'Game'},
            'begin': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expire': ('django.db.models.fields.DateTimeField', [], {}),
            'headline': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'name_away': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name_home': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'num_away': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_home': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'outcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_away': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'price_home': ('django.db.models.fields.IntegerField', [], {'default': '50'})
        },
        u'Guess.person': {
            'Meta': {'ordering': "('point', 'point_per_game')", 'object_name': 'Person'},
            'expertise': ('django.db.models.fields.TextField', [], {'default': "'N/A'"}),
            'game': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lose': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'point': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'point_per_game': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Guess']