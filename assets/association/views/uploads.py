import os
import mimetypes
from django import shortcuts
from django import http
from django.views.static import was_modified_since
from django.utils.http import http_date

from ..models.invoice import Invoice


def serve_upload(request, invoice_path):
    path = 'invoices/' + invoice_path
    upload = shortcuts.get_object_or_404(Invoice, document=path)
    fullpath = upload.document.path

    if not request.user.is_authenticated():
        return http.HttpResponseForbidden()

    statobj = os.stat(fullpath)
    mimetype, encoding = mimetypes.guess_type(fullpath)
    mimetype = mimetype or 'application/octet-stream'
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return http.HttpResponseNotModified(mimetype=mimetype)
    response = http.HttpResponse(open(fullpath, 'rb').read(),
                                 mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    response["Content-Length"] = statobj.st_size
    if encoding:
        response["Content-Encoding"] = encoding
    return response
