# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameTag'
        db.create_table(u'Guess_gametag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'Guess', ['GameTag'])

        # Adding model 'PersonTag'
        db.create_table(u'Guess_persontag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'Guess', ['PersonTag'])

        # Deleting field 'Person.expertise'
        db.delete_column(u'Guess_person', 'expertise')

        # Deleting field 'Person.point_per_game'
        db.delete_column(u'Guess_person', 'point_per_game')

        # Deleting field 'Person.index'
        db.delete_column(u'Guess_person', 'index')

        # Deleting field 'Game.index'
        db.delete_column(u'Guess_game', 'index')

        # Deleting field 'Game.game_type'
        db.delete_column(u'Guess_game', 'game_type')


    def backwards(self, orm):
        # Deleting model 'GameTag'
        db.delete_table(u'Guess_gametag')

        # Deleting model 'PersonTag'
        db.delete_table(u'Guess_persontag')

        # Adding field 'Person.expertise'
        db.add_column(u'Guess_person', 'expertise',
                      self.gf('django.db.models.fields.TextField')(default='N/A'),
                      keep_default=False)

        # Adding field 'Person.point_per_game'
        db.add_column(u'Guess_person', 'point_per_game',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'Person.index'
        db.add_column(u'Guess_person', 'index',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Game.index'
        db.add_column(u'Guess_game', 'index',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Game.game_type'
        db.add_column(u'Guess_game', 'game_type',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=50),
                      keep_default=False)


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
            'event': ('django.db.models.fields.IntegerField', [], {}),
            'expire': ('django.db.models.fields.DateTimeField', [], {}),
            'headline': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name_away': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name_home': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'num_away': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_home': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'outcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_away': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'price_home': ('django.db.models.fields.IntegerField', [], {'default': '50'})
        },
        u'Guess.gametag': {
            'Meta': {'object_name': 'GameTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'Guess.history': {
            'Meta': {'object_name': 'History'},
            'cur_price': ('django.db.models.fields.FloatField', [], {}),
            'cur_time': ('django.db.models.fields.DateTimeField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Guess.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Guess.message': {
            'Meta': {'object_name': 'Message'},
            'betting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Guess.Betting']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Guess.Person']"}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verbal': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'Guess.person': {
            'Meta': {'ordering': "('point', 'win')", 'object_name': 'Person'},
            'game': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lose': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'default': "'cat.jpg'", 'max_length': '100'}),
            'point': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Guess.persontag': {
            'Meta': {'object_name': 'PersonTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'Guess.proposal': {
            'Meta': {'object_name': 'Proposal'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'game_cate': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'game_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Guess.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
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