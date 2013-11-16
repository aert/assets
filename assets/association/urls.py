from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from .views.students import StudentsView
from .views.students import StudentsViewDetail
from .views.treasury import TreasuryView
from .views.accounts import AccountDetailView
from .views.accounts import AccountLogoutView
from .views.accounts import AccountLoginView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'association.views',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('students')), name='home'),

    # Students
    url(r'^students$', StudentsView.as_view(), name='students'),
    url(r'^students/(?P<id>\d+)/$', StudentsViewDetail.as_view(), name='students-detail'),

    # Treasury
    url(r'^treasury$', TreasuryView.as_view(), name='treasury'),

    # Account
    url(r'^account/(?P<pk>\d+)/$', AccountDetailView.as_view(), name='account-detail'),
    url(r'^logout$', AccountLogoutView.as_view(), name='account-logout'),
    url(r'^login$', AccountLoginView.as_view(), name='account-login'),

    # Admin
    url(r'^admin', include(admin.site.urls)),
)
