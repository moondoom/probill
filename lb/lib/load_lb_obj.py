from suds.client import Client
from suds import WebFault
from settings import *


cl = Client(LB_SOAP_URL)
cl.service.Login(LB_USERNAME, LB_PASSWORD)