from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from probill.billing.models import TrafficDetail, TrafficByPeriod




class Command(BaseCommand):
    args = '<counter>'
    help = 'Handler for billing status'

    def handle(self, *args, **options):
        from elasticsearch import Elasticsearch, client, exceptions
        if len(args) == 1:
            command = args[0]
            if command == 'export_detail':
                es = Elasticsearch()
                es_c = client.IndicesClient(es)
                es_c.delete(index='traffic_detail')
                query = TrafficDetail.objects.filter(datetime__gt=(datetime.now() - timedelta(days=1)),
                                                     datetime__lt=datetime.now())

                for x in query:
                    es.index(index='traffic_detail', doc_type='TrafficDetail', id=x.id, body={
                        "@timestamp": x.datetime,
                        "src_ip": str(x.src_ip),
                        "dst_ip": str(x.dst_ip),
                        "count": x.count
                    })
            if command == 'export_period':
                es = Elasticsearch()
                es_c = client.IndicesClient(es)
                try:
                    es_c.delete(index='traffic_by_period')
                except exceptions.NotFoundError as e:
                    print "Not found :)"
                    pass
                es_c.create(index='traffic_by_period')
                es_c.put_mapping(index='traffic_by_period', doc_type='TrafficByPeriod', body={
                    "properties": {
                        "login": {"type": "string", "index": "not_analyzed"},
                        "tariff": {"type": "string", "index": "not_analyzed"},
                        "qac": {"type": "string", "index": "not_analyzed"}
                    }
                })
                query = TrafficByPeriod.objects.filter(datetime__gt=(datetime.now() - timedelta(days=1)),
                                                       datetime__lt=datetime.now())
                query = query.prefetch_related("account", "tariff", "qac_class")

                for x in query:
                    if x.qac_class:
                        qac_name = unicode(x.qac_class.name)
                    else:
                        qac_name = "External"
                    es.index(index='traffic_by_period', doc_type='TrafficByPeriod', id=x.id, body={
                        "@timestamp": x.datetime,
                        "login": unicode(x.account),
                        "tariff": unicode(x.tariff),
                        "qac": qac_name,
                        "count": x.count
                    })

        else:
            raise CommandError('Invalid args length')