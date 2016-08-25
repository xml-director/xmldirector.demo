
import json

import plone.api
from zope.annotation import IAnnotations
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView


KEY = 'xmldirector-content-tree'


class Publication(BrowserView):

    @property
    def annotation(self):
        annotation = IAnnotations(self.context)
        anno = annotation.get(KEY)
        if anno is None:
            annotation[KEY] = dict()
            return {}
        return anno

    def save_tree(self, name='tree'):
        alsoProvides(self.request, IDisableCSRFProtection)

        if not name:
            name = datetime.utcnow().isoformat()
        data = json.loads(self.request.BODY)
        anno = self.annotation
        anno[name] = data
        self.request.response.setStatus(200)

    def connector(self):
        catalog = plone.api.portal.get_tool('portal_catalog')
        if not self.context.connectors:
            return None
        uid = self.context.connectors[0]
        brains = catalog(UID=uid)
        if not brains:
            return None
        return brains[0].getObject()

    def connector_url(self):
        catalog = plone.api.portal.get_tool('portal_catalog')
        if not self.context.connectors:
            raise ValueError('No connector configured')
        uid = self.context.connectors[0]
        brains = catalog(UID=uid)
        if not brains:
            raise ValueError('No connector found')
        connector = brains[0].getObject()
        return connector.absolute_url()

    def load_tree(self, name='tree'):
        anno = self.annotation
        if not name in anno:
            self.request.response.setStatus(404)
            return 'Key "{}" not found in tree'.format(name)
        return json.dumps(anno[name])

    def get_tree_data(self, path, mode):

        catalog = plone.api.portal.get_tool('portal_catalog')
        if not self.context.connectors:
            raise ValueError('No connector configured')
        uid = self.context.connectors[0]
        brains = catalog(UID=uid)
        if not brains:
            raise ValueError('No connector found')
        connector = brains[0].getObject()
        
        dirs = []
        files = []

        handle = connector.get_handle()
        for name, info in handle.ilistdirinfo(path, dirs_only=True):
            tooltip = u'{}, {}'.format(
                path + '/' + name,
                info['modified_time'].isoformat())
            dirs.append(dict(title=name,
                folder=True,
                lazy=True,
                tooltip=tooltip,
                extraClasses="src-node",
                modified_time=info['modified_time'].isoformat(),
                key=path + '/' + name,
                path=path + '/' + name))

        for name, info in handle.ilistdirinfo(path, files_only=True):
            tooltip = u'{}, {}, {}'.format(
                path + '/' + name,
                info['st_size'],
                info['modified_time'].isoformat())
            files.append(dict(title=name,
                folder=False,
                tooltip=tooltip,
                extraClasses="src-node",
                st_size=info['st_size'],
                modified_time=info['modified_time'].isoformat(),
                key=path + '/' + name,
                path=path + '/' + name))

        dirs = sorted(dirs, key=lambda d: d['title'])
        files = sorted(files, key=lambda d: d['title'])
        return json.dumps(dirs + files)
