from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.conf import settings
from .site import SiteAssets
from .views.uploads import serve_upload

from django.contrib import admin
admin.site = SiteAssets()
admin.autodiscover()

private_url = settings.PROTECTED_MEDIA_URL.strip("/")

urlpatterns = patterns(
    'association.views',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index')),
        name='home'),
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    # Uploads
    url(r'^' + private_url + '/invoices/(?P<invoice_path>.+)', serve_upload),
)
