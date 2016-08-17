from Products.Five.browser import BrowserView



class FormRenderingContext(object):

    def get(self, key, default=None):
        # do data lookup here
        value = key
        return value

    def form_action(self, widget, data):
        # create and return form action URL
        return 'http://example.com/form_action'

    def save(self, widget, data):
        # extract and save form data
        pass

    def next(self, request):
        # compute and return next URL
        return 'http://example.com/form_action_succeed'


message_factory = lambda x,default: x


class YAFOWIL(BrowserView):

    def form_renderer(self):
        import yafowil.loader
        from yafowil.yaml import parse_from_YAML

        rendering_context = FormRenderingContext()
        form = parse_from_YAML('xmldirector.demo.demo:test_form.yaml',
                               context=rendering_context,
                               message_factory=message_factory)
        return form()
