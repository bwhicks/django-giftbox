import os
from django.core.exceptions import ImproperlyConfigured
from django.views.static import serve
from django.http import HttpResponse
try:
    # py 2
    import urlparse as parse
except ImportError:
    # py 3
    import urllib.parse as parse

GOT_MAGIC = False
try:
    import magic
    GOT_MAGIC = True
except ImportError:
    pass


def get_mime(filepath):
    """
    Use python-magic to get the mime type of a file.

    Args:
        filepath (str): Path to the file to be sniffed by magic

    Returns:
        str: Returns a string representing the mime type of the file.
    """

    return magic.from_file(filepath, mime=True)


def send_dev_server(request, filename, **kwargs):
    """
    Send a file using Django's development server.

    Args:
        request (HttpRequest): An instance of :class:`django.http.HttpRequest`
        filename (str): name of the file to be served

    Keyword Args:
        doc_root (str): Valid path for Django's server to 'xsend'

    Returns:
        FileResponse: An instance of class:`django.http.FileResponse`.

    """
    doc_root = kwargs['doc_root']

    response = serve(request, filename, doc_root)
    # Django tries to pick an intelligent mime type
    # If magic, use it to help out
    if kwargs['use_magic']:
        if GOT_MAGIC:
            response['Content-Type'] = get_mime(
                os.path.join(doc_root, filename)
            )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def xsendfile(request, filename, **kwargs):
    """
    Send a file using an HTTP X-Sendfile or X-Accel-Redirect response.

    Args:
        request (HttpRequest): An instance of :class:`django.http.HttpRequest`
        filename (str): Name of the file to be served

    Keyword Args:

        sendfile_url (str): Xsendfile url to pass as part of http response.
        doc_root (str): Valid path to folder containing file, for magic to read

    Returns:
        HttpResponse: An instance of :class:`django.http.HttpResponse`.

    """

    base_url = kwargs['sendfile_url']
    url = parse.urljoin(base_url, filename)
    response = HttpResponse()

    response['X-Sendfile'] = url
    response['X-Accel-Redirect'] = url
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    # Delete default 'Content-Type', which indicates HTML, and let web server
    # try to get it right.
    del response['Content-Type']
    # If magic available and not explicitly disabled, use it to help out
    if kwargs['use_magic']:
        if GOT_MAGIC:
            if 'doc_root' not in kwargs or not kwargs['doc_root']:
                raise ImproperlyConfigured('If using python-magic, '
                                           '"doc_root" required.')
            doc_root = kwargs['doc_root']
            response['Content-Type'] = get_mime(os.path.join(doc_root, filename))
    return response
