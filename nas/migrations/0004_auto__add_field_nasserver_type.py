# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'NasServer.type'
        db.add_column('nas_nasserver', 'type', self.gf('django.db.models.fields.CharField')(default='freebsd_ipfw', max_length='20'), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'NasServer.type'
        db.delete_column('nas_nasserver', 'type')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 13, 20, 11, 47, 585609)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 13, 20, 11, 47, 585528)'}),
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
            'ip': ('probill.lib.networks.IPAddressField', [], {'unique': 'True', 'db_index': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'mac': ('probill.lib.networks.MACAddressField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Manager']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Subscriber']"}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Tariff']", 'null': 'True', 'blank': 'True'})
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
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Region']", 'null': 'True'})
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
            'traffic_cost': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nas.dhcpserver': {
            'Meta': {'object_name': 'DHCPServer'},
            'dns_first': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dns_second': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nas.NasServer']"})
        },
        'nas.dhcpsubnet': {
            'Meta': {'object_name': 'DHCPSubnet'},
            'default_router': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dhcp_server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nas.DHCPServer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subnet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nas.IPInterface']"})
        },
        'nas.ipinterface': {
            'Meta': {'object_name': 'IPInterface'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iface': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nas.NetworkInterface']"}),
            'network': ('probill.lib.networks.IPNetworkField', [], {})
        },
        'nas.nasserver': {
            'Meta': {'object_name': 'NasServer'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mng_ip': ('probill.lib.networks.IPAddressField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'freebsd_ipfw'", 'max_length': "'20'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'nas.netflowsource': {
            'Meta': {'object_name': 'NetFlowSource'},
            'file_dir': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'file_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nas.NasServer']"})
        },
        'nas.networkinterface': {
            'Meta': {'object_name': 'NetworkInterface'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nas.NasServer']"})
        },
        'nas.uplink': {
            'Meta': {'ordering': "['nas', 'priority', 'ipfw_nat_id']", 'unique_together': "(('nas', 'ipfw_nat_id'),)", 'object_name': 'UpLink'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipfw_nat_id': ('django.db.models.fields.IntegerField', [], {}),
            'local_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'nas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nas.NasServer']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'remote_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        'nas.uplinkpolice': {
            'Meta': {'ordering': "['nat_address', 'priority']", 'object_name': 'UpLinkPolice'},
            'accounts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['billing.Account']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nat_address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nas.UpLink']"}),
            'network': ('probill.lib.networks.IPNetworkField', [], {'default': "'0.0.0.0/32'", 'null': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        }
    }

    complete_apps = ['nas']
