from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text

from ._common_ import CHOICES_PAYMENT_TYPE
from ._common_ import APP_LABEL
from .student import Student


###############################################################################
# EARNING
###############################################################################

@python_2_unicode_compatible
class Earning(models.Model):
    CHOICES_EARNING_TYPE = (
        (1, _('subscription (internal)')),
        (2, _('other (internal)')),
        (10, _('external')),
    )

    payment_date = models.DateField(
        _('payment date'), default=datetime.datetime.now)
    earning_type = models.PositiveSmallIntegerField(
        _('earning type'), choices=CHOICES_EARNING_TYPE)
    amount = models.DecimalField(_('amount'), max_digits=15, decimal_places=2)
    label = models.CharField(_('label'), max_length=250)
    description = models.TextField(_('description'), blank=True)
    payment_type = models.PositiveSmallIntegerField(
        _('payment type'), choices=CHOICES_PAYMENT_TYPE)

    from_student = models.ForeignKey(Student, verbose_name=_('from student'),
                                     null=True, blank=True)
    from_other = models.CharField(_('from other'), max_length=250, blank=True)

    has_invoice = models.BooleanField(_('has invoice ?'), default=False,
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

    def is_internal(self):
        return self.earning_type != 10
    is_internal.admin_order_field = 'earning_type'
    is_internal.boolean = True
    is_internal.short_description = _('internal ?')
