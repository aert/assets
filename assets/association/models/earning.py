from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text

from ._common_ import CHOICES_PAYMENT_TYPE
from ._common_ import APP_LABEL


###############################################################################
# EARNING TYPE
###############################################################################

@python_2_unicode_compatible
class EarningType(models.Model):
    label = models.CharField(_('label'), max_length=50, unique=True)
    is_internal = models.BooleanField(_('internal'), default=False)

    class Meta:
        ordering = ['is_internal', 'label']
        verbose_name = _('type')
        verbose_name_plural = _('types')
        app_label = APP_LABEL

    def __str__(self):
        return smart_text(self.label)


###############################################################################
# EARNING
###############################################################################

@python_2_unicode_compatible
class Earning(models.Model):
    payment_date = models.DateField(
        _('payment date'), default=datetime.datetime.now)
    earning_type = models.ForeignKey(
        EarningType, verbose_name=('type'))
    amount = models.DecimalField(_('amount'), max_digits=15, decimal_places=2)
    label = models.CharField(_('label'), max_length=250)
    description = models.TextField(_('description'), blank=True)
    payment_type = models.PositiveSmallIntegerField(
        _('payment type'), choices=CHOICES_PAYMENT_TYPE)

    has_invoice = models.BooleanField(_('has invoice'), default=False,
                                      editable=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = _('earning')
        verbose_name_plural = _('earnings')
        app_label = APP_LABEL

    def __str__(self):
        return smart_text('{}: {}'.format(self.payment_date, self.label))
