
import sys
import os
import lxml.etree
import plone.api
import grampg
import defusedxml.lxml
import transaction
import pkg_resources
from Products.CMFPlone.factory import addPloneSite
from AccessControl.SecurityManagement import newSecurityManager
from xmldirector.plonecore.interfaces import IConnectorSettings
from plone.app.textfield.value import RichTextValue
from pp.client.plone.interfaces import IPPClientPloneSettings
from xmldirector.bookalope.interfaces import IBookalopeSettings
from plone import namedfile
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from plone.namedfile import NamedImage


extension_ids = [
    'plonetheme.barceloneta:default', 
    'xmldirector.demo:default', 
    'pp.client.plone:default', 
    'xmldirector.crex:default', 
    'xmldirector.bookalope:default', 
]

mode = sys.argv[-1]
if mode == 'docker':
    connector_url = u'http://localhost:8080/exist/webdav/db'
elif mode == 'local':
    connector_url = u'http://localhost:6080/exist/webdav/db'
else:
    raise ValueError('mode must be "local" or "docker"')

admin_pw = grampg.PasswordGenerator().of().between(100, 200, 'letters').done().generate()

uf = app.acl_users
user = uf.getUser('admin')

#uf._doChangeUser('admin', admin_pw, ('Manager',), ())
newSecurityManager(None, user.__of__(uf))
if 'xml-director' in app.objectIds():
    app.manage_delObjects('xml-director')

addPloneSite(app, 'xml-director', extension_ids=extension_ids)

site = app['xml-director']
#site.portal_quickinstaller.uninstallProducts(['xmldirector.plonecore'])
#site.portal_quickinstaller.installProducts(['xmldirector.plonecore'])

site.manage_delObjects(['events', 'news', 'Members'])
pr = site.portal_registration
pr.addMember('demo', 'demo', roles=('Editor','Reader', 'Manager'))

registry = getUtility(IRegistry)
settings = registry.forInterface(IConnectorSettings)
settings.connector_url = connector_url
settings.connector_username = u'admin'
settings.connector_password = u'onkopedia' if mode == 'local' else u'admin'

settings = registry.forInterface(IPPClientPloneSettings)
settings.server_url = u'https://pp-server.zopyx.com'
settings.server_username = u'demo'
settings.server_password = u'demo' 
#
registry = getUtility(IRegistry)
settings = registry.forInterface(IBookalopeSettings)
settings.bookalope_beta = False
settings.bookalope_api_key = u'051d17836932453f8bc962a442a35543'

import_dir = os.path.join(pkg_resources.get_distribution('xmldirector.demo').location, 'democontent', 'images')

image = plone.api.content.create(type='Image', container=site, id='logo', title='Logo')
img_data = open(os.path.join(import_dir, 'xmldirector.png'), 'rb').read()
image.image = namedfile.NamedBlobImage(img_data, filename=u'logo.png', contentType='image/png')
image.reindexObject()
image.exclude_from_nav = True
image.reindexObject()


frontpage_text = """
<br/>
<p>Login with username <b>demo</b> and password <b>demo</b>.</p>
<br/>
<p>
<ul>
<li><a href="http://pythonhosted.org/xmldirector.plonecore/demo.html">Demo documentation</a</li>
<li><a href="http://pythonhosted.org/xmldirector.plonecore/">Complete XML Director documentation</a</li>
<li><a href="http://www.xml-director.info">XML Director project site</a></li>
</ul>
</p>
"""

page = site['front-page']
try:
    page.setTitle('Welcome to the XML Director demo site')
except:
#    page.title = u'Welcome to the XML Director demo site'
    pass

try:
    page.setDescription(None)
except AttributeError:
#    page.description = None
    pass

try:
    page.setText(frontpage_text)
except AttributeError:
    page.text = RichTextValue(unicode(frontpage_text, 'utf-8'), 'text/html', 'text/html')


try:
    page.setPresentation(False)
except AttributeError:
    pass

page.reindexObject()

folder = plone.api.content.create(type='Folder', container=site, id='crex-docx-xml', title='CREX: DOCX-to-XML')
folder.setLayout('crex-upload-form')

folder = plone.api.content.create(type='Folder', container=site, id='bible', title='Bible XML')

import_dir = os.path.join(pkg_resources.get_distribution('xmldirector.demo').location, 'democontent', 'bible')
for name in os.listdir(import_dir):
    dok = plone.api.content.create(
        type='xmldirector.demo.bibledocument',
        container=folder,
        id=name,
        title=name)
    bible_content = open(os.path.join(import_dir, name)).read()
    dok.xml_set('xml_content', unicode(bible_content, 'utf-8'))
    dok.reindexObject()

folder = plone.api.content.create(type='Folder', container=site, id='mods', title='Bibliography XML (MODS)')
import_dir = os.path.join(pkg_resources.get_distribution('xmldirector.demo').location, 'democontent', 'mods')
for name in os.listdir(import_dir):
    if not name.endswith('.xml'):
        continue
    dok = plone.api.content.create(
        type='xmldirector.demo.modsdocument',
        container=folder,
        id=name,
        title=name)
    content = open(os.path.join(import_dir, name)).read()
    dok.xml_set('xml_content', unicode(content, 'utf-8'))
    dok.reindexObject()

folder = plone.api.content.create(type='Folder', container=site, id='musicxml', title='MusicXML')
import_dir = os.path.join(pkg_resources.get_distribution('xmldirector.demo').location, 'democontent', 'musicxml')
for name in os.listdir(import_dir):
    if not name.endswith('.xml'):
        continue
    dok = plone.api.content.create(
        type='xmldirector.demo.musicxml',
        container=folder,
        id=name,
        title=name)
    content = open(os.path.join(import_dir, name)).read()
    try:
        dok.xml_set('xml_content', unicode(content, 'utf-8'))
    except UnicodeDecodeError:
        dok.xml_set('xml_content', unicode(content, 'utf-16'))
    dok.reindexObject()

folder = plone.api.content.create(type='Folder', container=site, id='shakespeare', title='Shakespeare XML')
import_dir = os.path.join(pkg_resources.get_distribution('xmldirector.demo').location, 'democontent', 'shakespeare')

for name in sorted(os.listdir(import_dir)):

    if not name.endswith('.xml'):
        continue

    fname = os.path.join(import_dir, name)
    with open(fname, 'rb') as fp:
        xml = unicode(fp.read(), 'utf8')
        root = defusedxml.lxml.fromstring(xml.encode('utf8'))
        title = root.xpath('//title')[0].text
        dok = plone.api.content.create(
                type='xmldirector.demo.xmldocument',
                container=folder,
                id=name,
                title=title)

        dok.xml_set('xml_content', xml)
        dok.xml_xpath = u'field=xml_content,xpath=//title/text()'
        dok.reindexObject()
print 'commited'
transaction.commit()
