__author__ = 'animage'

import os, sys
from django.core.management import setup_environ

os.chdir(os.path.join(os.path.dirname(sys.argv[0]),".."))
sys.path.append(os.getcwd())
import settings
setup_environ(settings)