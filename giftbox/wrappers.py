from django.views.static import serve
from django.http import HttpResponse
import sys
try:
    import urlparse as parse
except ImportError:
    import urllib.parse as parse


def send_dev_server(request, filename, **kwargs):

    doc_root = kwargs['doc_root']

    response = serve(request, filename, doc_root)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def xsendfile(request, filename, **kwargs):

    base_url = kwargs['sendfile_url']
    url = parse.urljoin(base_url, filename)
    response = HttpResponse()

    response['X-Sendfile'] = url
    response['X-Accel-Redirect'] = url
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    del response['Content-Type']
    return response
