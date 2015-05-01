
import sys
import os
import lxml.etree
import plone.api
import grampg
import transaction
import pkg_resources
from Products.CMFPlone.factory import addPloneSite
from AccessControl.SecurityManagement import newSecurityManager
from xmldirector.plonecore.interfaces import IWebdavSettings
from plone.app.textfield.value import RichTextValue
from pp.client.plone.interfaces import IPPClientPloneSettings
from plone import namedfile
from plone.registry.interfaces import IRegistry
from zope.component import getUtility



admin_pw = grampg.PasswordGenerator().of().between(100, 200, 'letters').done().generate()

uf = app.acl_users
user = uf.getUser('admin')

#uf._doChangeUser('admin', admin_pw, ('Manager',), ())
newSecurityManager(None, user.__of__(uf))
if 'xml-director' in app.objectIds():
    app.manage_delObjects('xml-director')

try:

    addPloneSite(app, 'xml-director', create_userfolder=True, extension_ids=['plonetheme.sunburst:default', 'xmldirector.demo:default', 'pp.client.plone:default'])
except:
    addPloneSite(app, 'xml-director', extension_ids=['plonetheme.barceloneta:default', 'xmldirector.plonecore:default', 'xmldirector.demo:default', 'pp.client.plone:default'])

site = app['xml-director']
#site.portal_quickinstaller.uninstallProducts(['xmldirector.plonecore'])
#site.portal_quickinstaller.installProducts(['xmldirector.plonecore'])

print 'commited'
transaction.commit()
