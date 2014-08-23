# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DateTimeVariable'
        db.create_table('billing_datetimevariable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
            ('value', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('billing', ['DateTimeVariable'])


    def backwards(self, orm):
        # Deleting model 'DateTimeVariable'
        db.delete_table('billing_datetimevariable')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'billing.account': {
            'Meta': {'object_name': 'Account'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auto_block': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'block_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ip': ('probill.lib.networks.IPAddressField', [], {'default': "'0.0.0.0'", 'null': 'True', 'db_index': 'True', 'blank': "'True'"}),
            'login': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'mac': ('probill.lib.networks.MACAddressField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Manager']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '301'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Subscriber']"}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Tariff']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'billing.accounthistory': {
            'Meta': {'object_name': 'AccountHistory'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_id': ('django.db.models.fields.IntegerField', [], {}),
            'owner_type': ('django.db.models.fields.CharField', [], {'default': "'man'", 'max_length': '3'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Subscriber']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'billing.accountlog': {
            'Meta': {'object_name': 'AccountLog'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Account']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_status': ('django.db.models.fields.IntegerField', [], {}),
            'old_status': ('django.db.models.fields.IntegerField', [], {})
        },
        'billing.datetimevariable': {
            'Meta': {'object_name': 'DateTimeVariable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'value': ('django.db.models.fields.DateTimeField', [], {})
        },
        'billing.manager': {
            'Meta': {'object_name': 'Manager'},
            'father_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'system_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'billing.osmppay': {
            'Meta': {'object_name': 'OsmpPay'},
            'command': ('django.db.models.fields.IntegerField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osmp_txn_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'pay_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'process_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'prv_txn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.AccountHistory']", 'null': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'billing.periodiclog': {
            'Meta': {'object_name': 'PeriodicLog'},
            'code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {})
        },
        'billing.qosandcost': {
            'Meta': {'ordering': "['-id']", 'object_name': 'QosAndCost'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'qos_speed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subnets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['billing.Subnets']", 'symmetrical': 'False'}),
            'traffic_cost': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'billing.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'billing.subnets': {
            'Meta': {'object_name': 'Subnets'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('probill.lib.networks.IPNetworkField', [], {})
        },
        'billing.subscriber': {
            'Meta': {'ordering': "['first_name', 'last_name', 'father_name']", 'object_name': 'Subscriber'},
            'address_flat': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'address_house': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_type': ('django.db.models.fields.CharField', [], {'default': "'fl'", 'max_length': '2'}),
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'document': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'need_change_password': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Manager']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Region']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'billing.tariff': {
            'Meta': {'object_name': 'Tariff'},
            'archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'qac_class': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['billing.QosAndCost']", 'null': 'True', 'blank': 'True'}),
            'qos_speed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rental': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rental_period': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'speed_up': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'speed_up_end': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(6, 0)'}),
            'speed_up_start': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(22, 0)'}),
            'traffic_cost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'traffic_threshold': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'use_traffic_threshold': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'billing.tariffhistory': {
            'Meta': {'object_name': 'TariffHistory'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'set_data': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Tariff']"})
        },
        'billing.trafficbyperiod': {
            'Meta': {'object_name': 'TrafficByPeriod'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Account']"}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'count': ('django.db.models.fields.FloatField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qac_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.QosAndCost']", 'null': 'True', 'blank': 'True'}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Tariff']", 'null': 'True', 'blank': 'True'})
        },
        'billing.trafficdetail': {
            'Meta': {'object_name': 'TrafficDetail', 'db_table': "'tdcore'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Account']", 'null': 'True', 'blank': 'True'}),
            'count': ('django.db.models.fields.FloatField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'dst_ip': ('probill.lib.networks.IPAddressField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src_ip': ('probill.lib.networks.IPAddressField', [], {})
        },
        'billing.trustpay': {
            'Meta': {'object_name': 'TrustPay'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Manager']", 'null': 'True', 'blank': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Subscriber']"}),
            'trust_days': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'billing.visapay': {
            'Meta': {'object_name': 'VisaPay'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'check_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'check_req_body': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'check_resp_body': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'end': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gpb_trx_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pay_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pay_req_body': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'pay_resp_body': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Subscriber']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['billing']