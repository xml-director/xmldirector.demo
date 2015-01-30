# -*- coding: utf-8 -*-

################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

import logging
import datetime
import pprint

import plone.api
import zope.interface
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations
from BTrees.OOBTree import OOBTree

LOG = logging.getLogger('xmldirector.demo')

