from django.contrib.admin.sites import AdminSite
from django.conf.urls import patterns, url

from .views import dashboard


class AdminMixin(object):
    """Mixin for AdminSite to allow custom dashboard views."""

    def __init__(self, *args, **kwargs):
        return super(AdminMixin, self).__init__(*args, **kwargs)

    def get_urls(self):
        """
           Add our dashboard view to the admin urlconf.
           Deleted the default index.
        """
        urls = super(AdminMixin, self).get_urls()
        del urls[0]
        custom_url = patterns(
            '',
            url(r'^$', self.admin_view(dashboard.index), name="index")
        )

        return custom_url + urls


class SiteAssets(AdminMixin, AdminSite):
    """
    A Django AdminSite with the AdminMixin to allow registering custom
    dashboard view.
    """
