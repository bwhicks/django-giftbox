from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .wrappers import send_dev_server, send_xfile


class GiftBox(object):

    def __init__(self, request, **kwargs):

        self.request = request
        self.wrapper = None
        self.kwargs = dict()

        server = request.META.get('SERVER_SOFTWARE', None)
        if server is not None and \
                'WSGIServer' in server:
            self.wrapper = send_dev_server

        gbs = getattr(settings, 'GIFTBOX_SETTINGS', None)
        if not gbs:
            raise ImproperlyConfigured('Please configure GIFTBOX_SETTINGS.')
        if 'type' in gbs:
            if gbs['type'] == 'dev':
                self.wrapper = send_dev_server
            elif gbs['type'] == 'prod':
                self.wrapper = send_xfile

        if self.wrapper == send_xfile:
            self.kwargs['sendfile_url'] = gbs['sendfile_url'] \
                if 'sendfile_url' in gbs else None

        if self.wrapper == send_xfile:
            self.send = gbs['sendfile_url'] \
                if 'sendfile_url' in gbs else None

        self.doc_root = gbs['doc_root'] if 'doc_root' in gbs else None

        self.kwargs.update(kwargs)

    def send(self, filepath, **kwargs):

        send_func = self.wrapper
        obj_kwargs = self.kwargs

        if kwargs:
            obj_kwargs.update(self.kwargs)

        if 'doc_root' not in obj_kwargs:
            raise ImproperlyConfigured('GiftBox requires "doc_root" be set.')

        if 'sendfile_url' not in obj_kwargs \
                and isinstance(send_func, send_xfile):
            raise ImproperlyConfigured(
                'Giftbox requires "sendfile_url" be set when not running '
                'the development server.'
            )

        return send_func(self.request, filepath, **obj_kwargs)
