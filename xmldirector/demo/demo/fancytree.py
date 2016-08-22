
import json
from Products.Five.browser import BrowserView


class Fancytree(BrowserView):

    def get_tree_data(self, path, mode):
        files = []
        dirs = []
        handle = self.context.get_handle()
        for name, info in handle.ilistdirinfo(path, dirs_only=True):
            dirs.append(dict(title=name,
                folder=True,
                lazy=True,
                extraClasses="src-node",
                key=path + '/' + name,
                path=path + '/' + name))

        for name, info in handle.ilistdirinfo(path, files_only=True):
            files.append(dict(title=name,
                folder=False,
                extraClasses="src-node",
                key=path + '/' + name,
                path=path + '/' + name))

        dirs = sorted(dirs, key=lambda d: d['title'])
        files = sorted(files, key=lambda d: d['title'])

        return json.dumps(dirs + files)

