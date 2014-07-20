# coding=utf-8
from base64 import b64encode
from django.core.management.base import BaseCommand
from nas.models import *
from billing.models import PeriodicLog
from billing.views import serialize
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
        result = client.service.sendRequest(xml, sert)

        return dict(((k, v.encode('utf-8')) if isinstance(v, suds.sax.text.Text) else (k, v)) for (k, v) in result)

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

                        zf = StringIO(request['registerZipArchive'].decode('base64'))
                        zip_file = zipfile.ZipFile(zf, 'r')
                        print zip_file.read('dump.xml')
                        zip_file.close()
                        break
                    else:
                        if request['resultComment'] == 'запрос обрабатывается':
                            print 'Not ready yet.'
                            time.sleep(60)
                        else:
                            #Если это любая другая ошибка, выводим ее и прекращаем работу
                            print 'Error: %s' % request['resultComment']
                            break
        else:
            print 'Error: %s' % request['resultComment']
        if os.path.exists(req_path):
            os.remove(req_path)
        if os.path.exists(req_sig_path):
            os.remove(req_sig_path)






