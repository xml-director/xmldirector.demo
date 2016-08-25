
import json

from zope.annotation import IAnnotations
from Products.Five.browser import BrowserView


KEY = 'xmldirector-content-tree'

class Fancytree(BrowserView):

    @property
    def annotation(self):
        annotation = IAnnotations(self.context)
        anno = annotation.get(KEY)
        if anno is None:
            annotation[KEY] = dict()
            return {}
        return anno

    def save_tree(self, name='tree'):
        from zope.interface import alsoProvides
        from plone.protect.interfaces import IDisableCSRFProtection
        alsoProvides(self.request, IDisableCSRFProtection)

        if not name:
            name = datetime.utcnow().isoformat()
        data = json.loads(self.request.BODY)
        anno = self.annotation
        anno[name] = data
        self.request.response.setStatus(200)

    def load_tree(self, name='tree'):
        anno = self.annotation
        if not name in anno:
            self.request.response.setStatus(404)
            return 'Key "{}" not found in tree'.format(name)
        return json.dumps(anno[name])

    def get_tree_data(self, path, mode):
        files = []
        dirs = []
        handle = self.context.get_handle()
        for name, info in handle.ilistdirinfo(path, dirs_only=True):
            tooltip = u'{}, {}'.format(
                path + '/' + name,
                info['modified_time'].isoformat())
            dirs.append(dict(title=name,
                folder=True,
                lazy=True,
                tooltip=tooltip,
                extraClasses="src-node",
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
                key=path + '/' + name,
                path=path + '/' + name))

        dirs = sorted(dirs, key=lambda d: d['title'])
        files = sorted(files, key=lambda d: d['title'])

        return json.dumps(dirs + files)

