# coding=utf-8
from base64 import b64encode
from django.core.management.base import BaseCommand
from nas.models import *
from billing.models import PeriodicLog
from settings import *
from datetime import datetime
import time
import pytz
import suds
import subprocess

try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO
import zipfile
import xml.etree.ElementTree as etree
from billing.models import DateTimeVariable

class ZapretInfo:
    def getLastDumpDate(self):
        client = suds.client.Client(RIB_URL)
        result=client.service.getLastDumpDate()
        return result

    def sendRequest(self, requestFile, signatureFile):
        file = open(requestFile, "rb")
        data = file.read()
        file.close()
        xml = b64encode(data)

        file = open(signatureFile, "rb")
        data = file.readlines()
        file.close()

        if '-----' in data[0]:
            sert = ''.join(data[1:-1])
        else:
            #sert = ''.join(data)
            sert = b64encode(''.join(data))

        client = suds.client.Client(RIB_URL)
        if RIB_VERSION:
            result = client.service.sendRequest(xml, sert, RIB_VERSION)
        else:
            result = client.service.sendRequest(xml, sert)

        return dict(((k, v.encode('utf-8')) if isinstance(v, suds.sax.text.Text) else (k, v)) for (k, v) in result)

    def getLastDumpDateEx(self):
        pass

    def getResult(self,code):
        client = suds.client.Client(RIB_URL)
        result = client.service.getResult(code)

        return dict(((k, v.encode('utf-8')) if isinstance(v, suds.sax.text.Text) else (k, v)) for (k, v) in result)


class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'

    def handle(self, *args, **options):
        if not RIB_ENABLE:
            exit()
        if len(args) >= 1:
            if args[0] == 'last_load':
                now = time.time()
                last_load = DateTimeVariable.get('LastBlackListLoad')
                if last_load:
                    last_load = time.mktime(last_load.timetuple())
                    print int(now - last_load)
                else:
                    print int(now)
            exit()
        tz = pytz.timezone(TIME_ZONE)
        xml = '''<?xml version="1.0" encoding="windows-1251"?>
<request>
    <requestTime>{}</requestTime>
    <operatorName><![CDATA[{}]]></operatorName>
    <inn>{}</inn>
    <ogrn>{}</ogrn>
    <email>{}</email>
</request>
        '''.format(datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:%S.000%z')[:-2] + ':00',
                   RIB_ORG_NAME.decode('hex'),
                   RIB_INN,
                   RIB_OGRN,
                   RIB_EMAIL)
        xml = xml.decode('utf8').encode('cp1251')
        req_path = TMP_PATH + 'request.xml'
        req_sig_path = TMP_PATH + 'request.xml.sign'
        req_file = open(req_path, 'wb')
        req_file.write(xml)
        req_file.close()
        subprocess.call('{} smime -sign -gost89 -binary -noattr -in {} -out {} -signer {} -outform DER'.format(
            OPENSSL_COMMAND, req_path, req_sig_path, RIB_CERT_PATH
        ), shell=True)
        #exit()
        opener = ZapretInfo()
        request = opener.sendRequest(req_path, req_sig_path)
        if request['result']:
                code = request['code']
                print 'Got code {}'.format(code)
                print 'Trying to get result...'
                while 1:
                    request = opener.getResult(code)
                    if request['result']:
                        print 'Got it!'
                        print request['dumpFormatVersion']
                        zf = StringIO(request['registerZipArchive'].decode('base64'))
                        zip_file = zipfile.ZipFile(zf, 'r')
                        xml =zip_file.read('dump.xml')
                        zip_file.close()
                        xml_tree = etree.XML(xml)
                        ip_black_dict = {}
                        for content in xml_tree.iter('content'):
                            for element in ['ip', 'ipSubnet']:
                                for ip in content.iter(element):
                                    if ip.text.count('/'):
                                       address = ip.text
                                    else:
                                       address = ip.text + '/32'
                                    if address in ip_black_dict:
                                        ip_black_dict[address] += etree.tostring(content)
                                    else:
                                        ip_black_dict[address] = etree.tostring(content)
                        for acl in BlackListByIP.objects.all():
                            str_ip = str(acl.ip)
                            if str_ip in ip_black_dict:
                                if acl.description != ip_black_dict[str_ip]:
                                    print 'Update', acl.ip
                                    acl.description = ip_black_dict[str_ip]
                                    acl.save()
                                del ip_black_dict[str_ip]
                            else:
                                print 'Delete', acl.ip
                                acl.delete()
                        for ip in ip_black_dict:
                            print 'Add', ip
                            BlackListByIP(ip=ip, description=ip_black_dict[ip]).save()
                        DateTimeVariable.set('LastBlackListLoad',datetime.now())
                        break
                    else:
                        if request['resultComment'] == 'запрос обрабатывается':
                            print 'Not ready yet.'
                            time.sleep(60)
                        else:
                            #Если это любая другая ошибка, выводим ее и прекращаем работу
                            PeriodicLog.log('Script PROCESS_BLACKLIST Error: %s' % request['resultComment'], code=10)
                            break
        else:
            PeriodicLog.log('Script PROCESS_BLACKLIST Error: %s' % request['resultComment'], code=10)
        if os.path.exists(req_path):
            os.remove(req_path)
        if os.path.exists(req_sig_path):
            os.remove(req_sig_path)






