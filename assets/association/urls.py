from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from .site import SiteAssets

from django.contrib import admin
admin.site = SiteAssets()
admin.autodiscover()

urlpatterns = patterns(
    'association.views',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index')), name='home'),
    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
