from iptv.models import SSIPTVChannel
from django.core.management.base import BaseCommand

import httplib
import json


class Command(BaseCommand):
    args = ''
    help = 'Get SS-IPTV chanells list'

    def handle(self, *args, **options):
        query = SSIPTVChannel.objects.filter(is_local=False)
        channel_dict = {}
        for channel in query:
            channel_dict[channel.ss_id] = channel
        conn = httplib.HTTPConnection('api.ss-iptv.com', timeout=10)
        conn.request("GET", "/?action=getChannels")
        resp = conn.getresponse()
        play_list = json.load(resp)
        for channel in play_list:
            if channel['id'] in channel_dict:
                if channel['title'] != channel_dict[channel['id']]:
                    channel_dict[channel['id']].title = channel['title']
                    channel_dict[channel['id']].save()
                del channel_dict[channel['id']]
            else:
                SSIPTVChannel(ss_id=channel['id'],
                              ss_title=channel['title']).save()

        for k in channel_dict:
            channel_dict[k].delete()