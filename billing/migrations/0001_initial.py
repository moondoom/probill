# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PeriodicLog'
        db.create_table('billing_periodiclog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('code', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('billing', ['PeriodicLog'])

        # Adding model 'Manager'
        db.create_table('billing_manager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('father_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('billing', ['Manager'])

        # Adding model 'Subscriber'
        db.create_table('billing_subscriber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('login', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, db_index=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('document', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Manager'])),
            ('address_street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address_house', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('address_type', self.gf('django.db.models.fields.CharField')(default='fl', max_length=2)),
            ('address_flat', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('balance', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('billing', ['Subscriber'])

        # Adding model 'AccountHistory'
        db.create_table('billing_accounthistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Subscriber'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('owner_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('owner_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('billing', ['AccountHistory'])

        # Adding model 'Subnets'
        db.create_table('billing_subnets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('network', self.gf('probill.lib.networks.IPNetworkField')()),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
        ))
        db.send_create_signal('billing', ['Subnets'])

        # Adding model 'QosAndCost'
        db.create_table('billing_qosandcost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('traffic_cost', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('qos_speed', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('billing', ['QosAndCost'])

        # Adding M2M table for field subnets on 'QosAndCost'
        db.create_table('billing_qosandcost_subnets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('qosandcost', models.ForeignKey(orm['billing.qosandcost'], null=False)),
            ('subnets', models.ForeignKey(orm['billing.subnets'], null=False))
        ))
        db.create_unique('billing_qosandcost_subnets', ['qosandcost_id', 'subnets_id'])

        # Adding model 'Tariff'
        db.create_table('billing_tariff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('rental_period', self.gf('django.db.models.fields.CharField')(default='m', max_length=1)),
            ('rental', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('traffic_cost', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('qos_speed', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('billing', ['Tariff'])

        # Adding M2M table for field qac_class on 'Tariff'
        db.create_table('billing_tariff_qac_class', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tariff', models.ForeignKey(orm['billing.tariff'], null=False)),
            ('qosandcost', models.ForeignKey(orm['billing.qosandcost'], null=False))
        ))
        db.create_unique('billing_tariff_qac_class', ['tariff_id', 'qosandcost_id'])

        # Adding model 'Account'
        db.create_table('billing_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Subscriber'])),
            ('login', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, db_index=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('tariff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Tariff'], null=True, blank=True)),
            ('ip', self.gf('probill.lib.networks.IPAddressField')(unique=True, db_index=True)),
            ('mac', self.gf('probill.lib.networks.MACAddressField')(max_length=17, null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Manager'])),
            ('block_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('auto_block', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('billing', ['Account'])

        # Adding model 'TariffHistory'
        db.create_table('billing_tariffhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('set_data', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Account'])),
            ('tariff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Tariff'])),
        ))
        db.send_create_signal('billing', ['TariffHistory'])

        # Adding model 'TrafficByPeriod'
        db.create_table('billing_trafficbyperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Account'])),
            ('tariff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Tariff'])),
            ('qac_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.QosAndCost'], null=True, blank=True)),
            ('count', self.gf('django.db.models.fields.FloatField')()),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('billing', ['TrafficByPeriod'])

        # Adding model 'TrafficDetail'
        db.create_table('tdcore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('src_ip', self.gf('probill.lib.networks.IPAddressField')()),
            ('dst_ip', self.gf('probill.lib.networks.IPAddressField')()),
            ('count', self.gf('django.db.models.fields.FloatField')()),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Account'], null=True, blank=True)),
        ))
        db.send_create_signal('billing', ['TrafficDetail'])


    def backwards(self, orm):
        
        # Deleting model 'PeriodicLog'
        db.delete_table('billing_periodiclog')

        # Deleting model 'Manager'
        db.delete_table('billing_manager')

        # Deleting model 'Subscriber'
        db.delete_table('billing_subscriber')

        # Deleting model 'AccountHistory'
        db.delete_table('billing_accounthistory')

        # Deleting model 'Subnets'
        db.delete_table('billing_subnets')

        # Deleting model 'QosAndCost'
        db.delete_table('billing_qosandcost')

        # Removing M2M table for field subnets on 'QosAndCost'
        db.delete_table('billing_qosandcost_subnets')

        # Deleting model 'Tariff'
        db.delete_table('billing_tariff')

        # Removing M2M table for field qac_class on 'Tariff'
        db.delete_table('billing_tariff_qac_class')

        # Deleting model 'Account'
        db.delete_table('billing_account')

        # Deleting model 'TariffHistory'
        db.delete_table('billing_tariffhistory')

        # Deleting model 'TrafficByPeriod'
        db.delete_table('billing_trafficbyperiod')

        # Deleting model 'TrafficDetail'
        db.delete_table('tdcore')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 28, 19, 46, 32, 569787)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 28, 19, 46, 32, 569717)'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('probill.lib.networks.IPAddressField', [], {'unique': 'True', 'db_index': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'mac': ('probill.lib.networks.MACAddressField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Manager']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Subscriber']"}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Tariff']", 'null': 'True', 'blank': 'True'})
        },
        'billing.accounthistory': {
            'Meta': {'object_name': 'AccountHistory'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_id': ('django.db.models.fields.IntegerField', [], {}),
            'owner_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Subscriber']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
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
            'document': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Manager']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'billing.tariff': {
            'Meta': {'object_name': 'Tariff'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'qac_class': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['billing.QosAndCost']", 'null': 'True', 'blank': 'True'}),
            'qos_speed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rental': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rental_period': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'traffic_cost': ('django.db.models.fields.FloatField', [], {'default': '0'})
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
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Tariff']"})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['billing']
