# -*- coding: utf-8 -*-

################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

import os
import uuid
import unittest2
import plone.api
from fs.contrib.davfs import DAVFS
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.testing import z2
from plone.registry.interfaces import IRegistry

from zope.component import getUtility
from zope.configuration import xmlconfig
from xmldirector.plonecore.interfaces import IWebdavSettings
from AccessControl.SecurityManagement import newSecurityManager

import xmldirector.plonecore
import plone.app.dexterity
import pp.client.plone



from xmldirector.plonecore.tests.base import PolicyFixture


class PolicyFixture(PolicyFixture):

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup

        applyProfile(portal, 'xmldirector.demo:default')
        super(PolicyFixture, self).setUpPloneSite(portal)


POLICY_FIXTURE = PolicyFixture()
POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(POLICY_FIXTURE,), name='PolicyFixture:Integration')


class TestBase(unittest2.TestCase):

    layer = POLICY_INTEGRATION_TESTING

    @property
    def portal(self):
        return self.layer['portal']

    def login(self, uid='god'):
        """ Login as manager """
        user = self.portal.acl_users.getUser(uid)
        newSecurityManager(None, user.__of__(self.portal.acl_users))
