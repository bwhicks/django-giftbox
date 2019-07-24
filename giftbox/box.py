from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .wrappers import send_dev_server, xsendfile


class GiftBox(object):
    """Container class for sendfile wrappers

    Attributes:
        request (HttpRequest): Instance of :class:`django.http.HttpRequest`
        wrapper (function): Instance of either
            :func:`~giftbox.wrappers.send_dev_server` or
            :func:`~giftbox.wrappers.xsendfile`
        kwargs (dict): A dictionary containing kwargs passed to the object,
            used by the wrappers to accept settings whether
            from ``settings.py`` or :class:`GiftBox` object on creation.
    """

    def __init__(self, request, **kwargs):
        """
        Create a :class:`GiftBox` instance.

        Args:
            request (HttpRequest): Instance of
            :class:`django.http.HttpRequest`.

        Keyword Args:
            doc_root (str): Valid filepath for Django's development server
                                to 'xsend' files.
        """

        # Object has access to ``self.request``, ``self.kwargs``, and
        # ``self.wrapper``.
        self.request = request
        self.wrapper = None
        self.kwargs = dict()

        # Check for development server running
        server = request.META.get('SERVER_SOFTWARE', None)
        if server is not None and \
                'WSGIServer' in server:
            self.wrapper = send_dev_server

        # Check for GIFTBOX_SETTINGS
        gbs = getattr(settings, 'GIFTBOX_SETTINGS', None)
        if not gbs:
            raise ImproperlyConfigured('Please configure GIFTBOX_SETTINGS.')

        # Use settings to determine wrapper, if not running development server.
        if 'type' in gbs and not self.wrapper:
            if gbs['type'] == 'dev':
                self.wrapper = send_dev_server
            elif gbs['type'] == 'prod':
                self.wrapper = xsendfile

        self.kwargs['doc_root'] = gbs.get('doc_root', None)
        self.kwargs['use_magic'] = gbs.get('use_magic', None)

        try:
            import magic
            self.kwargs['has_magic'] = True
            # set if unspecified since magic has been detected
            if self.kwargs['use_magic'] is None:
                self.kwargs['use_magic'] = True
        except ImportError:
            if self.kwargs['use_magic']:
                raise ImproperlyConfigured('To enable magic for mime-typing, install python-magic and libmagic.')
            self.kwargs['has_magic'] = False

        self.kwargs.update(kwargs)

        if not self.kwargs['doc_root']:
            raise ImproperlyConfigured('You must specify a "doc_root"')

    def send(self, filename, **kwargs):
        """
        Return an HTTP Response to send the specified file.

        Args:

            filename (str): The name of a file to serve.
            doc_root (str): Valid path for Django's server to 'xsend'
            use_magic (bool): whether or not to pythonmagic
        """
        obj_kwargs = self.kwargs.copy()
        obj_kwargs.update(kwargs)
        # If somehow a wrapper hasn't been set yet.
        if not self.wrapper:
            raise ImproperlyConfigured('You must specify a wrapper before '
                                       'using send.')
        return self.wrapper(self.request, filename, **obj_kwargs)
