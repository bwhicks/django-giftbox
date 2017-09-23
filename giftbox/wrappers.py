import os
import sys
from django.views.static import serve
from django.http import HttpResponse

if sys.version_info < (3, 0):
    import urllib as urllib
else:
    import urllib.parse as urllib


def send_dev_server(request, filename, **kwargs):

    doc_root = kwargs['doc_root']

    response = serve(request, filename, doc_root)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def xsendfile(request, filename, **kwargs):

    base_url = kwargs['sendfile_url']
    url = urllib.urljoin(base_url, filename)
    response = HttpResponse()

    response['X-Sendfile'] = url
    response['X-Accel-Redirect'] = url
    return response
