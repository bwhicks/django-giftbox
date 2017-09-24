from django.views.static import serve
from django.http import HttpResponse
try:
    import urlparse as parse
except ImportError:
    import urllib.parse as parse


def send_dev_server(request, filename, **kwargs):
    """
    Send a file using Django's development server.

    :param request: An instance of :class:`django.http.HttpRequest`
    :type request: object.
    :param filename: Name of the file to be served.
    :type filename: str.
    :param **kwargs: See notes below.
    :returns: :class:~`django.http.FileResponse` object.

    :Keyword Arguments:
        * *doc_root* (``str``) --
            Valid filepath for Django's development server to 'xsend'

    """
    doc_root = kwargs['doc_root']

    response = serve(request, filename, doc_root)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def xsendfile(request, filename, **kwargs):
    """
    Send a file using an HTTP X-Sendfile or X-Accel-Redirect response.
    :param request: An instance of :class:`django.http.HttpRequest`
    :type request: object.
    :param filename: Name of the file to be served.
    :type filename: str.
    :returns: :class:~`django.http.HttpResponse` object.

    :Keyword Arguments:
        * *sendfile_url* (``str``) --
            Xsendfile url to pass as part of http response.
    """

    base_url = kwargs['sendfile_url']
    url = parse.urljoin(base_url, filename)
    response = HttpResponse()

    response['X-Sendfile'] = url
    response['X-Accel-Redirect'] = url
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    # Delete default 'Content-Type', which indicates HTML
    del response['Content-Type']
    return response
